# GLSL

vertex_shader = """
#version 450
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform float valor;
uniform vec3 pointLight;

out vec3 outColor;
out vec2 outTexCoords;

void main()
{
    vec4 norm = vec4(normal, 0.0);

    vec4 pos = vec4(position, 1.0) + norm * valor;
    pos = modelMatrix * pos;

    vec4 light = vec4(pointLight, 1.0);

    float intensity = dot(modelMatrix * norm, normalize(light - pos));

    gl_Position = projectionMatrix * viewMatrix * pos;

    outColor = vec3(1.0,1.0 - valor * 2,1.0-valor * 2) * intensity * 2;
    outTexCoords = texCoords;
}
"""


fragment_shader = """
#version 450
layout (location = 0) out vec4 fragColor;

in vec3 outColor;
in vec2 outTexCoords;

uniform sampler2D tex;

void main()
{
    fragColor = vec4(outColor, 1) * texture(tex, outTexCoords);
}
"""


vertex_toon_shader = """
#version 450
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform float valor;
uniform vec3 pointLight;

out vec3 outColor;
out vec2 outTexCoords;
out float outIntensity;

void main()
{
    vec4 norm = vec4(normal, 0.0);

    vec4 pos = vec4(position, 1.0) + norm * valor;
    pos = modelMatrix * pos;

    vec4 light = vec4(pointLight, 1.0);

    outIntensity = dot(modelMatrix * norm, normalize(light - pos));

    gl_Position = projectionMatrix * viewMatrix * pos;

    outColor = vec3(1.0,1.0 - valor * 2,1.0-valor * 2);
    outTexCoords = texCoords;
}
"""

fragment_toon_shader = """
#version 450
layout (location = 0) out vec4 fragColor;

in vec3 outColor;
in vec2 outTexCoords;
in float outIntensity;

uniform sampler2D tex;

void main()
{

    float curIntensity;

    if (outIntensity > 0.8){
        curIntensity = 0.8;
    }else if (outIntensity > 0.6){
        curIntensity = 0.6;
    }else if (outIntensity > 0.4){
        curIntensity = 0.4;
    }else {
        curIntensity = 0.2;
    }


    fragColor = vec4(outColor, 1) * texture(tex, outTexCoords) * (curIntensity * 3);
}
"""

fragment_termic_shader = """
#version 450
layout (location = 0) out vec4 fragColor;

// in vec3 outColor;
in vec2 outTexCoords;
in float outIntensity;

uniform sampler2D tex;

void main()
{

    vec3 color;

    if (outIntensity > 0.8){
        color = vec3(0.99, 0.88, 0.61);
    }else if (outIntensity > 0.6){
        color = vec3(0.99 , 0.8, 0.27);
    }else if (outIntensity > 0.4){
        color = vec3(0.76, 0.09, 0.57);
    }else {
        color = vec3(0.007, 0.0, 0.6);
    }


    fragColor = vec4(color, 1) * texture(tex, outTexCoords) * (outIntensity * 2);
}
"""

vertex_rainbow_shader = """
#version 450
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float valor;
uniform vec3 randomColor;

out vec3 outColor;
out vec2 outTexCoords;

void main()
{
    vec4 norm = vec4(normal, 0.0);

    vec4 pos = vec4(position, 1.0) + norm * valor;
    pos = modelMatrix * pos;

    gl_Position = projectionMatrix * viewMatrix * pos;

    outColor = randomColor;
    outTexCoords = texCoords;
}
"""

fragment_rainbow_shader = """
#version 450
layout (location = 0) out vec4 fragColor;

in vec3 outColor;
in vec2 outTexCoords;

uniform sampler2D tex;


void main()
{
    vec3 color = outColor;
    fragColor = vec4(color, 1) * texture(tex, outTexCoords);

}
"""


vertex_static_shader = """
#version 450
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float valor;
uniform vec3 randomColor;

out vec2 outTexCoords;

void main()
{
    vec4 norm = vec4(normal, 0.0);

    vec4 pos = vec4(position, 1.0) + norm * valor;
    pos = modelMatrix * pos;

    gl_Position = projectionMatrix * viewMatrix * pos;

    outTexCoords = texCoords;
}
"""

fragment_static_shader = """
#version 450
layout (location = 0) out vec4 fragColor;

in vec2 outTexCoords;

uniform sampler2D tex;
uniform vec2 random2;

float random (vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main()
{
    vec2 st = gl_FragCoord.xy / random2.xy;
    st *= 10.0; 
    vec2 ipos = floor(st);  
    vec2 fpos = fract(st);  
    vec3 color = vec3(random( ipos ));

    fragColor = vec4(color, 1) * texture(tex, outTexCoords);
}
"""



