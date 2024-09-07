#version 460 core

layout(location = 0) out vec4 fragColor;

struct Light {
  vec3 position;
  vec3 Ia;
  vec3 Id;
  vec3 Is;
};

uniform Light light;

vec3 getLight(vec3 color) {
  vec3 ambient = light.Ia;
  return color * ambient;
}

void main() {
  vec3 color = vec3(0.1, 0.9, 0.1);
  color = getLight(color);
  fragColor = vec4(color, 1.0);
}