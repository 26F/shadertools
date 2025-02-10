
import cv2
from OpenGL.GL import*
import glfw
from glfw import*
import sys


from random import randrange

if len(sys.argv) < 2:
	# usage where n is frame number
	print("usage: python3 shader2png.py 1920x1080 myshader.frag n")
	sys.exit(0)

import time
import numpy as np



# Frames
# preprocessingbuffer = Queue(maxsize=50)


# Canvas vertices which are passed to the vertex shader to specify the drawing plane.
vertices = np.array([
    -1.0, -1.0, 0.0, 0.0,
     1.0, -1.0, 1.0, 0.0,
    -1.0,  1.0, 0.0, 1.0,
     1.0, -1.0, 1.0, 0.0,
    -1.0,  1.0, 0.0, 1.0,
     1.0,  1.0, 1.0, 1.0
], dtype=np.float32)

fps = 60
dimensions = [int(x) for x in sys.argv[1].split('x')]

# vertex shader source code:
vertexshsrc = """
#version 330 core

layout (location = 0) in vec2 position;            
layout (location = 1) in vec2 inTexCoord;

out vec2 texCoord;

void main()
{
   
    texCoord = inTexCoord;
    gl_Position = vec4(position.x, position.y, 0.0f, 1.0f);


}
"""



# Video class for the videos to hold their data and meta.
class Video():
	def __init__(self, src, dimensions, fps, totalframes):
		self.src = src
		self.dimensions = dimensions
		self.fps = fps
		self.totalframes = totalframes



class GLCtx():
	def __init__(self, filename, vao, vbo, framebufferid, vertexshid, fragmentshid, shaderprogramid):
		self.filename = filename, 
		self.vao = vao
		self.vbo = vbo
		self.fragmentshid = fragmentshid
		self.vertexshid = vertexshid
		self.fragmentshid = fragmentshid
		self.shaderprogramid = shaderprogramid


# Load input video and get its frame rate, 
# total number of frames and resultion
def inputVideo(filename):
	src = cv2.VideoCapture(filename)

	# Did you pass filename correctlt?
	assert(src.isOpened())

	fps = int(src.get(cv2.CAP_PROP_FPS))
	dimensions = [int(src.get(cv2.CAP_PROP_FRAME_WIDTH)), int(src.get(cv2.CAP_PROP_FRAME_HEIGHT))]
	totalframes = int(src.get(cv2.CAP_PROP_FRAME_COUNT))

	return Video(src, dimensions, fps, totalframes)


# Pass the input video to the output video to 
# get needed data
def outputVideo(filename, video):
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	dst = None
	return Video(dst, video.dimensions, video.fps, video.totalframes)


# Hidden rendering window
def renderingWindow(dimensions):
	# Can init glfw?
	assert(glfw.init())
	
	# Make sure viewport is correct size
	glViewport(0, 0, dimensions[0], dimensions[1])

	# Window should be hidden
	glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

	# Window creation here
	window = glfw.create_window(dimensions[0], dimensions[1], "", None, None)

	# Creation succcess and correct dimensions
	assert(window)
	w, h = glfw.get_framebuffer_size(window)
	assert(w == dimensions[0] and h == dimensions[1])
	glfw.make_context_current(window)

	return window


# Rendering Context (OpenGL stuff)
# pass name of fragment shader
def renderingGLCtx(filename, resolution):

	fragmentshsrc = open(filename).read()
	assert(fragmentshsrc)

	# Vertex array object
	vao = glGenVertexArrays(1)
	glBindVertexArray(vao)

	# Vertex buffer object
	vbo = glGenBuffers(1)

	# Vertex attributes are bound to vertex buffer object through id
	glBindBuffer(GL_ARRAY_BUFFER, vbo)

	# Buffer the vertices which are used like a canvas for drawing
	glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

	# Set the vertex attribute storage types so it knows WTF is going on
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0))
	glEnableVertexAttribArray(0)
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0))
	glEnableVertexAttribArray(1)

	# We can unbind now.
	glBindVertexArray(0)

	# We need to generate (frame) buffers now 
	framebufferid = glGenFramebuffers(1)


	# Compile the vertex shader
	vertexshid = glCreateShader(GL_VERTEX_SHADER)
	glShaderSource(vertexshid, vertexshsrc)
	glCompileShader(vertexshid)


	# Create and compile the fragment shader
	fragmentshid = glCreateShader(GL_FRAGMENT_SHADER)
	glShaderSource(fragmentshid, fragmentshsrc)
	glCompileShader(fragmentshid)


	# Create the shader program and link it and everything
	shaderprogramid = glCreateProgram()
	glAttachShader(shaderprogramid, vertexshid)
	glAttachShader(shaderprogramid, fragmentshid)
	glLinkProgram(shaderprogramid)

	# Use the program
	glUseProgram(shaderprogramid)

	glUniform2fv(glGetUniformLocation(shaderprogramid, "iResolution"), 1, resolution)

	glBindFramebuffer(GL_FRAMEBUFFER, framebufferid)
	glBindFramebuffer(GL_FRAMEBUFFER, 0)
	glBindVertexArray(vao)

	return GLCtx(filename, vao, vbo, framebufferid, vertexshid, fragmentshid, shaderprogramid)

def mutateFrame(frameid, fps, dimensions, ctx, window):
	itime = frameid * (1.0 / fps)	
	glUniform1f(glGetUniformLocation(ctx.shaderprogramid, "iTime"), int(sys.argv[3]) * 0.05);	

	glClearColor(0, 0, 0, 1)
	glClear(GL_COLOR_BUFFER_BIT)

	glDrawArrays(GL_TRIANGLES, 0, 6)

	glfw.swap_buffers(window)
	glfw.poll_events()

	frame = glReadPixels(0, 0, dimensions[0], dimensions[1], GL_BGR, GL_UNSIGNED_BYTE)
	return np.frombuffer(frame, dtype=np.uint8).reshape(dimensions[1], dimensions[0], 3)

framenum = 0

def process(ctx, rwindow, fps, dimensions):
	global kill
	global framenum

	# dst.src.write(mutateFrame(framenum, fps, dimensions, ctx, rwindow))
	# Ensure image is produced by putting this line here
	mutateFrame(framenum, fps, dimensions, ctx, rwindow)
	mutateFrame(framenum, fps, dimensions, ctx, rwindow)
	cv2.imwrite("{}.png".format(int(sys.argv[3])), mutateFrame(framenum, fps, dimensions, ctx, rwindow))

# dst = outputVideo("{}.mp4".format(randrange(0, 10000000000000000000)), Video(None, dimensions, fps, kill))

rwindow = renderingWindow(dimensions)
glctx = renderingGLCtx(sys.argv[2], dimensions)

print("working...")
process(glctx, rwindow, fps, dimensions)

