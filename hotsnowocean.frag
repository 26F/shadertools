
#version 330 core

in vec2 texCoord;

uniform vec2 iResolution;
uniform float iTime;
out vec4 fragColor;

vec2 fragCoord = gl_FragCoord.xy;

#define SQR(X) ((X) * (X))


float ray(vec3 rayOrigin, vec3 rayDirection)
{


    float dt = 0.01;
    float limit = 10.0;
    
    for (float t = 0.0; t < limit; t += dt)
    {
    
    
        vec3 p = rayOrigin + rayDirection * t;

        if (p.y * 23.0 >= (cos(p.x * 13.0 + iTime) * sin(p.z * 13.0 + iTime)))
        {
        
            
            return t;
        }
    
    }
    
    
    return 0.0;

}



void main()
{
   
    
    vec2 uv = fragCoord.xy / iResolution.xy * 2.0 - 1.0;
    uv.x *= (iResolution.x / iResolution.y);
    uv.y = -uv.y;
    
    vec3 shade = vec3(0.3);
    
    
    vec3 rayOrigin = vec3(uv, -1.0);
    vec3 fixation = vec3(abs(cos(iTime * 0.01)), abs(sin(iTime * 0.001)), 0.5);
    vec3 rayDirection = fixation - rayOrigin;
    float r = ray(rayOrigin, rayDirection + vec3(0.02,  0.001, 0.001));
    float g = ray(rayOrigin, rayDirection + vec3(0.01,   0.01,   0.029));
    float b = ray(rayOrigin, rayDirection + vec3(0.01, 0.004, 0.018));   
    
    
    fragColor = vec4(vec3(pow(r, 5.0), pow(g, 5.0), pow(b, 5.0)) + shade, 1.0);
   
   
}