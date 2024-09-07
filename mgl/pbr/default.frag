#version 460 core

layout(location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
  vec3 position;
  vec3 color;
};

struct Material {
  vec3 Ka;
  float Km;
  float Kr;
  float Kao;
};

uniform vec3 camPos;
uniform Light light;
uniform Light light2;
uniform Light light3;
uniform Light light4;
uniform Material material;
uniform sampler2D u_texture_0;

const float PI = 3.14159265359;
float DistributionGGX(vec3 N, vec3 H, float roughness);
float GeometrySchlickGGX(float NdotV, float roughness);
float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness);
vec3 fresnelSchlick(float cosTheta, vec3 F0);
vec3 fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}
float DistributionGGX(vec3 N, vec3 H, float roughness) {
    float a = roughness*roughness;
    float a2 = a*a;
    float NdotH = max(dot(N, H), 0.0);
    float NdotH2 = NdotH*NdotH;
    float num = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;
    return num / denom;
}
float GeometrySchlickGGX(float NdotV, float roughness) {
    float r = (roughness + 1.0);
    float k = (r*r) / 8.0;
    float num = NdotV;
    float denom = NdotV * (1.0 - k) + k;
    return num / denom;
}
float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness) {
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    float ggx2 = GeometrySchlickGGX(NdotV, roughness);
    float ggx1 = GeometrySchlickGGX(NdotL, roughness);
    return ggx1 * ggx2;
}

vec3 calculateLight(vec3 N, vec3 V, Light light, vec3 F0) {
  // Per-light radiance
  vec3 L = normalize(light.position - fragPos);
  vec3 H = normalize(V + L);
  float distance = length(light.position - fragPos);
  float attenuation = 1.0; // / (distance * distance);
  vec3 radiance = light.color * attenuation;
  // Cook-torrance brdf
  float NDF = DistributionGGX(N, H, material.Kr);
  float G = GeometrySmith(N, V, L, material.Kr);
  vec3 F = fresnelSchlick(max(dot(H, V), 0.0), F0);
  vec3 kD = vec3(1.0) - F;
  kD *= 1.0 - material.Km;
  vec3 numerator = NDF * G * F;
  float denominator = 4.0 * max(dot(N, V), 0.0) * max(dot(N, L), 0.0) + 0.0001;
  vec3 specular = numerator / denominator;
  float NdotL = max(dot(N, L), 0.0);
  vec3 Lo = (kD * material.Ka / PI + specular) * radiance * NdotL;
  return Lo;
}

vec3 getLight(vec3 tex_color) {
  vec3 N = normalize(normal);
  vec3 V = normalize(camPos - fragPos);
  vec3 F0 = vec3(0.04); 
  F0 = mix(F0, material.Ka, material.Km);
  vec3 ambient = vec3(0.03) * material.Ka * material.Kao;
  
  vec3 Lo = vec3(0.0);
  //// PER LIGHT ////
  Lo += calculateLight(N, V, light, F0);
  Lo += calculateLight(N, V, light2, F0);
  Lo += calculateLight(N, V, light3, F0);
  Lo += calculateLight(N, V, light4, F0);
  //// LOOP END ////

  vec3 light_color = ambient + Lo;
  light_color = light_color / (light_color + vec3(1.0));
  light_color = pow(light_color, vec3(1.0/2.2));  
  
  // return mix(tex_color, tex_color * light_color, 0.5);
  // return mix(tex_color, light_color, 0.5);
  return tex_color * light_color;
}

void main() {
  vec3 color = texture(u_texture_0, uv_0).rgb;
  color = getLight(color);
  fragColor = vec4(color, 1.0);
}