import math
import moderngl_window


class App(moderngl_window.WindowConfig):
    window_size = 1600, 900
    resource_dir = 'programs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = moderngl_window.geometry.quad_fs()
        self.program = self.load_program(vertex_shader='vertex.glsl', fragment_shader='fragment.glsl')
        self.u_scroll = 3.0
        # Textures
        self.texture1 = self.load_texture_2d('../textures/test0.png')
        self.texture2 = self.load_texture_2d('../textures/hex.png')  # floor
        self.texture3 = self.load_texture_2d('../textures/white_marble1.png')  # walls
        self.texture4 = self.load_texture_2d('../textures/roof/texture3.jpg')  # roof
        self.texture5 = self.load_texture_2d('../textures/black_marble1.png')  # pedestal
        self.texture6 = self.load_texture_2d('../textures/green_marble1.png')  # sphere
        self.texture7 = self.load_texture_2d('../textures/roof/height3.png')  # roof bump
        # Uniforms
        self.program['u_scroll'] = self.u_scroll
        self.program['u_resolution'] = self.window_size
        self.program['u_texture1'] = 1
        self.program['u_texture2'] = 2
        self.program['u_texture3'] = 3
        self.program['u_texture4'] = 4
        self.program['u_texture5'] = 5
        self.program['u_texture6'] = 6
        self.program['u_texture7'] = 7
        self.texture1.use(location=1)
        self.texture2.use(location=2)
        self.texture3.use(location=3)
        self.texture4.use(location=4)
        self.texture5.use(location=5)
        self.texture6.use(location=6)
        self.texture7.use(location=7)

    def render(self, time, frame_time):
        self.update(time)
        self.ctx.clear()
        self.quad.render(self.program)

    def update(self, time):
        self.program['u_time'] = time
        self.program['u_mouse'] = (math.sin(time) * 200, math.sin(time) * 100)
        self.program['u_scroll'] = math.sin(time) * 0.5 + 3.0

    # def mouse_position_event(self, x, y, dx, dy):
    #     self.program['u_mouse'] = (x, y)

    # def mouse_scroll_event(self, x_offset, y_offset):
    #     self.u_scroll = max(1.0, self.u_scroll + y_offset)
    #     self.program['u_scroll'] = self.u_scroll


if __name__ == '__main__':
    moderngl_window.run_window_config(App)
