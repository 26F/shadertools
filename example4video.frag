#version 330 core

in vec2 texCoord;

// uniform vec2 iMouse;
uniform vec2 iResolution;
uniform float iTime;
uniform sampler2D iChannel0;
out vec4 fragColor;

vec2 fragCoord = gl_FragCoord.xy;

void main() 
{


    vec2 uv = fragCoord / iResolution.xy * 2.0 - 1.0;
    uv.x *= (iResolution.x / iResolution.y);

    // texture coordinates
    vec2 tc = fragCoord / iResolution.xy;

    // all we've done is switch the color channels from rgb
    // using swizzling
    vec3 colr = texture(iChannel0, tc).gbr;

    fragColor = vec4(colr, 1.0);
    
}
