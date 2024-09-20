import math
import glm
import moderngl
import numpy
import pygame


def generate_vertex_data(vertices, indices):
    data = [vertices[ind] for triangle in indices for ind in triangle]
    return numpy.array(data, dtype='f4')


class Terrain:
    def __init__(self, app, position=(0, 0, 0), width=40, step=1, curve=0.5, height_map_path="height_map"):
        self.app = app
        self.ctx = app.ctx
        self.position = glm.mat4(glm.translate(glm.mat4(1), glm.vec3(position)))

        # Read {app.base_path}/{app.textures_path}/{height_map_path}.png with pygame and numpy
        height_map, height_map_w, height_map_h = app.texture.get_image_data(f'{app.base_path}/{app.texture_path}/{height_map_path}.png')

        height_map_w = 90
        height_map_h = 90

        half_step = step / 2
        half_width = height_map_w / 2
        half_height = height_map_h / 2

        # Get value at 0,0 i.e. half_width, half_height; use this to place the terrain under the camera
        max_height = 100
        centre_height = height_map[math.floor(half_height)][math.floor(half_width)][0] / 255 * max_height

        vertices = []
        for z in range(1, height_map_h):
            for x in range(1, height_map_w):
                y1 = math.floor(height_map[z][x-step][0] / 255 * max_height - centre_height)
                y2 = math.floor(height_map[z][x][0] / 255 * max_height - centre_height)
                y3 = math.floor(height_map[z-step][x][0] / 255 * max_height - centre_height)
                y4 = math.floor(height_map[z-step][x-step][0] / 255 * max_height - centre_height)
                vertices.append((x-half_step-half_width, y1, z+half_step-half_height))
                vertices.append((x+half_step-half_width, y2, z+half_step-half_height))
                vertices.append((x+half_step-half_width, y3, z-half_step-half_height))
                vertices.append((x-half_step-half_width, y4, z-half_step-half_height))
        self.vertices = vertices

        # Generate indices
        indices = []
        for i in range(0, len(vertices) - 1, 4):
            indices.append((i, i + 2, i + 3))
            indices.append((i, i + 1, i + 2))
        self.indices = indices

        # Generate vertex data
        vertex_data = generate_vertex_data(vertices, indices)
        # Texture coordinates and texture indices
        texture_coords = []
        texture_indices = []
        for i in range(0, len(vertices) - 1, 4):
            # Randomize texture coordinates to rotate the texture
            rand_int = numpy.random.randint(4)
            if rand_int == 0:
                texture_coords.append((0, 0))
                texture_coords.append((1, 0))
                texture_coords.append((1, 1))
                texture_coords.append((0, 1))
            elif rand_int == 1:
                texture_coords.append((1, 0))
                texture_coords.append((1, 1))
                texture_coords.append((0, 1))
                texture_coords.append((0, 0))
            elif rand_int == 2:
                texture_coords.append((1, 1))
                texture_coords.append((0, 1))
                texture_coords.append((0, 0))
                texture_coords.append((1, 0))
            elif rand_int == 3:
                texture_coords.append((0, 1))
                texture_coords.append((0, 0))
                texture_coords.append((1, 0))
                texture_coords.append((1, 1))
            texture_indices.append((0, 2, 3))
            texture_indices.append((0, 1, 2))
        texture_coord_data = generate_vertex_data(texture_coords, texture_indices)
        vertex_data = numpy.hstack([texture_coord_data, vertex_data])
        self.vertex_data = numpy.array(vertex_data, dtype='f4')


class Ground():
    def __init__(self, app, position=(0, 0, 0), texture: str = 'dirt', terrain: Terrain = None, shader_name='ground'):
        self.app = app
        self.ctx = app.ctx
        self.position = glm.mat4(glm.translate(glm.mat4(1), glm.vec3(position)))
        self.terrain = terrain
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program(shader_name)
        self.vao = self.get_vao()
        self.tex_id = app.texture.get_alpha_texture(path=f'textures/{texture}.png')
        self.on_init()

    def on_init(self):
        # Texture
        self.shader_program['u_texture_0'] = self.tex_id
        # Light
        self.shader_program['light.color'].value = self.app.light.color
        # Position
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.position)
        # self.shader_program['camPos'].write = self.app.camera.position
        # Set point size
        self.ctx.point_size = 4

    def update(self):
        self.shader_program['m_view'].write(self.app.camera.m_view)
        # self.shader_program['camPos'].write = self.app.camera.position

    def render(self):
        self.app.texture.textures[self.tex_id].use(location=0)
        self.vao.render()
        # self.vao.render(moderngl.TRIANGLE_STRIP)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [
            (self.vbo, '2f 3f', 'in_texcoord_0', 'in_position'),
        ])
        return vao

    def get_vbo(self):
        return self.ctx.buffer(self.terrain.vertex_data)

    def get_shader_program(self, shader_name='default'):
        with open(f'{self.app.base_path}/{self.app.shader_path}/{shader_name}.vert', 'r') as f:
            vertex_shader_source = f.read()
        with open(f'{self.app.base_path}/{self.app.shader_path}/{shader_name}.frag', 'r') as f:
            fragment_shader_source = f.read()
        shader_program = self.ctx.program(
            vertex_shader=vertex_shader_source,
            fragment_shader=fragment_shader_source
        )
        return shader_program

    def get_model_matrix(self):
        return glm.mat4()
