#version 460 core

layout (location = 0) in vec3 in_texcoord_0;
layout (location = 1) in vec3 in_position;
layout (location = 2) in vec3 in_normal;

out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;
out vec4 shadow_coord;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_view_light;
uniform mat4 m_model;

const float tiny = 0.05;

// Bias matrix to convert the coordinates from [-1, 1] to [0, 1] from clip space to texture space
const mat4 m_shadow_bias = mat4(0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.5, 0.5, 0.5, 1.0);

void main() {
    const vec4 in_position4 = vec4(in_position, 1.0);

    uv_0 = in_texcoord_0.xy;
    normal = mat3(transpose(inverse(m_model))) * in_normal;
    fragPos = vec3(m_model * in_position4);
    gl_Position = m_proj * m_view * m_model * in_position4;

    shadow_coord = m_shadow_bias * m_proj * m_view_light * m_model * in_position4;
    shadow_coord.z -= tiny;
}