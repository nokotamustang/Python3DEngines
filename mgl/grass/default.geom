#version 460 core

layout (points) in;
layout (triangle_strip, max_vertices = 36) out;

out GS_OUT {
	vec2 textCoord;
	float colorVariation;
} gs_out;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;
uniform vec3 camPos;
uniform sampler2D u_wind;
uniform float u_time;

const float c_min_size = 0.4f;
const float LOD1 = 5.0f;
const float LOD2 = 10.0f;
const float LOD3 = 20.0f;
const float PI = 3.141592653589793;

float grass_size;

mat4 rotationX(in float angle);
mat4 rotationY(in float angle);
mat4 rotationZ(in float angle);
float random(vec2 st);
float noise(in vec2 st);
float fbm(in vec2 _st);

// vec4 vertexPosition[4];
// vertexPosition[0] = vec4(-0.25, 0.0, 0.0, 0.0); // down left
// vertexPosition[1] = vec4( 0.25, 0.0, 0.0, 0.0); // down right
// vertexPosition[2] = vec4(-0.25, 0.5, 0.0, 0.0); // up left
// vertexPosition[3] = vec4( 0.25, 0.5, 0.0, 0.0); // up right
// const vec4 vertexPosition[4] = vec4[4](vec4(-0.25, 0.0, 0.0, 0.0), vec4( 0.25, 0.0, 0.0, 0.0), vec4(-0.25, 0.5, 0.0, 0.0), vec4( 0.25, 0.5, 0.0, 0.0));
const vec4 v_pos_1 = vec4(-0.25, 0.0, 0.0, 0.0);
const vec4 v_pos_2 = vec4( 0.25, 0.0, 0.0, 0.0);
const vec4 v_pos_3 = vec4(-0.25, 0.5, 0.0, 0.0);
const vec4 v_pos_4 = vec4( 0.25, 0.5, 0.0, 0.0);

// vec2 textCoords[4];
// textCoords[0] = vec2(0.0, 0.0); // down left
// textCoords[1] = vec2(1.0, 0.0); // down right
// textCoords[2] = vec2(0.0, 1.0); // up left
// textCoords[3] = vec2(1.0, 1.0); // up right
// const vec2 textCoords[4] = vec2[4](vec2(0.0, 0.0), vec2(1.0, 0.0), vec2(0.0, 1.0), vec2(1.0, 1.0));
const vec2 t_coord_1 = vec2(0.0, 0.0);
const vec2 t_coord_2 = vec2(1.0, 0.0);
const vec2 t_coord_3 = vec2(0.0, 1.0);
const vec2 t_coord_4 = vec2(1.0, 1.0);

void emitGrassVertex(vec4 in_pos, mat4 modelWind, mat4 modelRandY, mat4 crossmodel, vec4 vertexPosition, vec2 textCoords) {
    gl_Position = m_proj * m_view * m_model * (in_pos + modelWind * modelRandY * crossmodel * (vertexPosition * grass_size));
    gs_out.textCoord = textCoords;
    gs_out.colorVariation = fbm(in_pos.xz);
    EmitVertex();
}

void createQuad(vec3 base_position, mat4 crossmodel) {
	vec4 in_pos = gl_in[0].gl_Position;

	// Wind
	vec2 windDirection = vec2(1.0, 1.0);
    float windStrength = 0.15f;
	vec2 uv = base_position.xz/10.0 + windDirection * windStrength * u_time;
	uv.x = mod(uv.x,1.0);
	uv.y = mod(uv.y,1.0);
	vec4 wind = texture(u_wind, uv);
	mat4 modelWind = (rotationX(wind.x*PI*0.75f - PI*0.25f) * rotationZ(wind.y*PI*0.75f - PI*0.25f));
	mat4 modelWindApply = mat4(1);

	// Random rotation on Y
	mat4 modelRandY = rotationY(random(base_position.zx)*PI);

	// Billboard creation
	// for (int i = 0; i < 4; ++i) {
	// 	if (i == 2 ) modelWindApply = modelWind;
    //     emitGrassVertex(in_pos, modelWindApply, modelRandY, crossmodel, vertexPosition[i], textCoords[i]);
    // }
    // Unrolled loop, which is faster in GLSL
    emitGrassVertex(in_pos, modelWindApply, modelRandY, crossmodel, v_pos_1, t_coord_1);
    emitGrassVertex(in_pos, modelWindApply, modelRandY, crossmodel, v_pos_2, t_coord_2);
    emitGrassVertex(in_pos, modelWind, modelRandY, crossmodel, v_pos_3, t_coord_3);
    emitGrassVertex(in_pos, modelWindApply, modelRandY, crossmodel, v_pos_4, t_coord_4);
    EndPrimitive();
}

void createGrass(int numberQuads) {
	if (numberQuads == 1) {
        const mat4 model0 = mat4(1.0f);
        createQuad(gl_in[0].gl_Position.xyz, model0);
    } else if (numberQuads == 2) {
        const mat4 model45 = rotationY(radians(45));
        const mat4 modelm45 = rotationY(-radians(45));
        createQuad(gl_in[0].gl_Position.xyz, model45);
        createQuad(gl_in[0].gl_Position.xyz, modelm45);
    } else if (numberQuads == 3) {
        const mat4 model0 = mat4(1.0f);
        const mat4 model45 = rotationY(radians(45));
        const mat4 modelm45 = rotationY(-radians(45));
        createQuad(gl_in[0].gl_Position.xyz, model0);
        createQuad(gl_in[0].gl_Position.xyz, model45);
        createQuad(gl_in[0].gl_Position.xyz, modelm45);
	}
}

void main() {
	float dist_length = length(gl_in[0].gl_Position.xyz - camPos); // Distance of position to camera
  grass_size = random(gl_in[0].gl_Position.xz) * (1.0f - c_min_size) + c_min_size;

	// Distance of position to camera
	float t = 6.0f; if (dist_length > LOD2) t *= 1.5f;
	dist_length += (random(gl_in[0].gl_Position.xz)*t - t/2.0f);

	// Change number of quad function of distance
	int lessDetails = 3;
	if (dist_length > LOD1) lessDetails = 2;
	if (dist_length > LOD2) lessDetails = 1;
	if (dist_length > LOD3) lessDetails = 0;

	// Create grass
	if (lessDetails != 1
		|| (lessDetails == 1 && (int(gl_in[0].gl_Position.x * 10) % 1) == 0 || (int(gl_in[0].gl_Position.z * 10) % 1) == 0)
		|| (lessDetails == 2 && (int(gl_in[0].gl_Position.x * 5) % 1) == 0 || (int(gl_in[0].gl_Position.z * 5) % 1) == 0)
	)
		createGrass(lessDetails);
}

mat4 rotationX( in float angle ) {
	return mat4(1.0, 0, 0, 0,
                0, cos(angle), -sin(angle), 0,
                0, sin(angle), cos(angle), 0,
                0, 0, 0, 1);
}

mat4 rotationY( in float angle ) {
	return mat4(cos(angle), 0, sin(angle), 0,
			 	0, 1.0, 0, 0,
				-sin(angle),	0, cos(angle), 0,
				0, 0, 0,	1);
}

mat4 rotationZ( in float angle ) {
	return mat4(cos(angle), -sin(angle), 0, 0,
			 	sin(angle), cos(angle), 0, 0,
				0, 0, 1, 0,
				0, 0, 0,	1);
}

float random (vec2 st) {
    return fract(sin(dot(st.xy,vec2(12.9898,78.233)))*43758.5453123);
}

float noise (in vec2 st) {
	vec2 i = floor(st);
	vec2 f = fract(st);
	// Four corners in 2D of a tile
	float a = random(i);
	float b = random(i + vec2(1.0, 0.0));
	float c = random(i + vec2(0.0, 1.0));
	float d = random(i + vec2(1.0, 1.0));
	// Smooth Interpolation
	// Cubic Hermine Curve.  Same as SmoothStep()
	vec2 u = f*f*(3.0-2.0*f);
	// u = smoothstep(0.,1.,f);
	// Mix 4 coorners percentages
	return mix(a, b, u.x) +
	(c - a)* u.y * (1.0 - u.x) +
	(d - b) * u.x * u.y;
}

#define NUM_OCTAVES 5
float fbm(in vec2 _st) {
	float v = 0.0;
	float a = 0.5;
	vec2 shift = vec2(100.0);
	// Rotate to reduce axial bias
	mat2 rot = mat2(cos(0.5), sin(0.5),
	-sin(0.5), cos(0.50));
	for (int i = 0; i < NUM_OCTAVES; ++i) {
		v += a * noise(_st);
		_st = rot * _st * 2.0 + shift;
		a *= 0.5;
	}
	return v;
}