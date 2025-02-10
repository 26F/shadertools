import numpy as np
from OpenGL.GL import*
import glfw
from glfw import*
import sys

res = [1920, 1080]

if len(sys.argv) < 2:
	print("usage: python3 shader2model.py myshader.frag 64")
	print("sampling using an n^3 grid so 64x64x64 would be the above sampling")


# Canvas vertices which are passed to the vertex shader to specify the drawing plane.
vertices = np.array([
    -1.0, -1.0, 0.0, 0.0,
     1.0, -1.0, 1.0, 0.0,
    -1.0,  1.0, 0.0, 1.0,
     1.0, -1.0, 1.0, 0.0,
    -1.0,  1.0, 0.0, 1.0,
     1.0,  1.0, 1.0, 1.0
], dtype=np.float32)

#amount of sampling
grid_spacing = int(sys.argv[2])

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


class GLCtx():
	def __init__(self, filename, vao, vbo, framebufferid, vertexshid, fragmentshid, shaderprogramid):
		self.filename = filename, 
		self.vao = vao
		self.vbo = vbo
		self.fragmentshid = fragmentshid
		self.vertexshid = vertexshid
		self.fragmentshid = fragmentshid
		self.shaderprogramid = shaderprogramid


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


def convert_2_model(gl_ctx, window):
	glClearColor(0, 0, 0, 1)
	glClear(GL_COLOR_BUFFER_BIT)

	glDrawArrays(GL_TRIANGLES, 0, 6)

	glfw.swap_buffers(window)

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


rwindow = renderingWindow(res)
glctx = renderingGLCtx(sys.argv[1], res)
convert_2_model(glctx, rwindow)