import glm
import numpy


class Cube:
    def __init__(self, app, albedo=(0.9, 0.1, 0.1), diffuse=0.8, specular=1.0,
                 ao: float = 1.0, position=(0, 0, 0),
                 texture: str = 'img'):
        self.app = app
        self.ctx = app.ctx
        self.position = glm.mat4(glm.translate(glm.mat4(1), glm.vec3(position)))
        self.albedo = 0.06 * glm.vec3(albedo)  # Ambient (Albedo)
        self.diffuse = diffuse * glm.vec3(albedo)  # Diffuse (Lambert)
        self.specular = specular * glm.vec3(albedo)  # Specular (Blinn-Phong)
        self.ao = ao
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.tex_id = app.texture.get_texture(path=f'textures/{texture}.png')
        self.on_init()

    def on_init(self):
        # Texture
        self.shader_program['u_texture_0'] = self.tex_id
        self.app.texture.textures[self.tex_id].use()
        # Light
        self.shader_program['light.position'].value = self.app.light.position
        self.shader_program['light.color'].value = self.app.light.color
        self.shader_program['light.strength'].value = self.app.light.strength
        # Second light
        self.shader_program['light2.position'].value = self.app.light2.position
        self.shader_program['light2.color'].value = self.app.light2.color
        self.shader_program['light2.strength'].value = self.app.light2.strength
        # Third light
        self.shader_program['light3.position'].value = self.app.light3.position
        self.shader_program['light3.color'].value = self.app.light3.color
        self.shader_program['light3.strength'].value = self.app.light3.strength
        # Fourth light
        self.shader_program['light4.position'].value = self.app.light4.position
        self.shader_program['light4.color'].value = self.app.light4.color
        self.shader_program['light4.strength'].value = self.app.light4.strength
        # Position
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.position)
        # Material: Albedo (rgb)
        self.shader_program['material.Ka'].value = self.albedo
        self.shader_program['material.Kd'].value = self.diffuse
        self.shader_program['material.Ks'].value = self.specular
        self.shader_program['material.Kao'].value = self.ao
        # Camera
        # self.shader_program['camPos'].write = self.app.camera.position

    def update(self):
        m_model = glm.rotate(self.position, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(m_model)
        # self.shader_program['camPos'].write = self.app.camera.position

    def render(self):
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [
            (self.vbo, '2f 3f 3f', 'in_texcoord_0', 'in_position', 'in_normal'),
        ])
        return vao

    def get_vertex_data(self, size=0.5):
        # Vertices
        vertices = [
            (-size, -size, size), (size, -size, size), (size, size, size), (-size, size, size),
            (-size, size, -size), (-size, -size, -size), (size, -size, -size), (size, size, -size)
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6),
        ]
        vertex_data = self.generate_vertex_data(vertices, indices)

        # Texture coordinates
        texture_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_indices = [(0, 2, 3), (0, 1, 2),
                           (0, 2, 3), (0, 1, 2),
                           (0, 1, 2), (2, 3, 0),
                           (2, 3, 0), (2, 0, 1),
                           (0, 2, 3), (0, 1, 2),
                           (3, 1, 2), (3, 0, 1)]
        texture_coord_data = self.generate_vertex_data(texture_coords, texture_indices)
        vertex_data = numpy.hstack([texture_coord_data, vertex_data])

        # Normals
        normals = [
            (0, 0, 1) * 6,
            (1, 0, 0) * 6,
            (0, 0, -1) * 6,
            (-1, 0, 0) * 6,
            (0, 1, 0) * 6,
            (0, -1, 0) * 6,
        ]
        normals = numpy.array(normals, dtype='f4').reshape(36, 3)
        vertex_data = numpy.hstack([vertex_data, normals])

        return numpy.array(vertex_data, dtype='f4')

    @staticmethod
    def generate_vertex_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype='f4')

    def get_vbo(self):
        return self.ctx.buffer(self.get_vertex_data())

    def get_shader_program(self, shader_name='default'):
        with open(f'{self.app.base_path}/{shader_name}.vert', 'r') as f:
            vertex_shader_source = f.read()
        with open(f'{self.app.base_path}/{shader_name}.frag', 'r') as f:
            fragment_shader_source = f.read()
        shader_program = self.ctx.program(
            vertex_shader=vertex_shader_source,
            fragment_shader=fragment_shader_source,
        )
        return shader_program
