Make your fragment shaders (GLSL) into high resolution images or use as video effects.

You'll need to install using pip3:

pip3 install opencv-python
pip3 install glfw

may need to use:

pip3 install PyOpenGL

Tested on linux mint and kali linux. 

Migrating a shader from shadertoy.com, you'll need to flip the y as in the hotsnowocean.frag example.

Usage:

shader2video.py

python3 shader2video.py 60 1920x1080 120 myshader.frag

can use up to 4k

shader2png.py

python3 shader2png.py 3840x2160 hotsnowocean.frag

