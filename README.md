Make your fragment shaders (GLSL) into high resolution images or use as video effects.

You'll need to install using pip3:

pip3 install opencv-python
pip3 install glfw

may need to use:

pip3 install PyOpenGL

Tested on linux mint and kali linux. 

Migrating a shader from shadertoy.com, you'll need to flip the y as in the hotsnowocean.frag example.

Usage:
python3 addshader2video.py myvideo.mp4 myshader.frag
Can also use
python3 addshader2video.py myvideo.mp4 myshader.frag 100
if you want to output a hundred frames instead of the entire video, to test how the shader looks.

