import glm
import moderngl
import numpy


class Grass:
    def __init__(self, app, position=(0, 0, 0),
                 texture: str = 'grass'):
        self.app = app
        self.ctx = app.ctx
        self.position = glm.mat4(glm.translate(glm.mat4(1), glm.vec3(position)))
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.tex_id = app.texture.get_alpha_texture(path=f'textures/{texture}.png')
        self.tex_id_wind = app.texture.get_basic_texture(path=f'textures/flowmap.png')
        self.on_init()

    def on_init(self):
        # Variables
        self.shader_program['u_time'].value = self.app.time
        # Texture
        self.shader_program['u_wind'] = self.tex_id_wind
        self.shader_program['u_texture_0'] = self.tex_id
        # Light
        self.shader_program['light.color'].value = self.app.light.color
        # Position
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.position)
        self.shader_program['camPos'].write = self.app.camera.position
        # Set point size
        self.ctx.point_size = 4

    def update(self):
        # m_model = glm.rotate(self.get_model_matrix(), self.app.time, glm.vec3(0, 1, 0))
        # self.shader_program['m_model'].write(m_model)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['u_time'].value = self.app.time
        self.shader_program['camPos'].write = self.app.camera.position

    def render(self):
        self.app.texture.textures[self.tex_id_wind].use(location=1)
        self.app.texture.textures[self.tex_id].use(location=0)
        self.vao.render(moderngl.POINTS)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [
            (self.vbo, '3f', 'in_position'),
        ])
        return vao

    def get_vertex_data(self):
        vertices = []
        n_wide = 40
        step = 0.1
        for x in numpy.arange(-n_wide, n_wide, step):
            for z in numpy.arange(-n_wide, n_wide, step):
                vertices.append((x, 0, z))
        return numpy.array(vertices, dtype='f4')

    def get_vbo(self):
        return self.ctx.buffer(self.get_vertex_data())

    def get_shader_program(self, shader_name='default'):
        with open(f'{self.app.base_path}/{shader_name}.vert', 'r') as f:
            vertex_shader_source = f.read()
        with open(f'{self.app.base_path}/{shader_name}.frag', 'r') as f:
            fragment_shader_source = f.read()
        with open(f'{self.app.base_path}/{shader_name}.geom', 'r') as f:
            geometry_shader_source = f.read()
        shader_program = self.ctx.program(
            vertex_shader=vertex_shader_source,
            fragment_shader=fragment_shader_source,
            geometry_shader=geometry_shader_source
        )
        return shader_program

    def get_model_matrix(self):
        return glm.mat4()
