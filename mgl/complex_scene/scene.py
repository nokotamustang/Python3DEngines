from model import *
from core import BaseScene


class Scene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        # Skybox
        self.skybox = AdvancedSkyBox(app)

    def load(self):
        app = self.app
        add = self.add_object
        # Floor
        n, step_size = 20, 2
        # for y in range(-n, 0, step_size):
        for x in range(-n, n, step_size):
            for z in range(-n, n, step_size):
                add(Cube(app, pos=(x, -2, z)))
        # Columns
        for i in range(9):
            add(Cube(app, pos=(15, i * step_size, -9 + i), tex_id=2))
            add(Cube(app, pos=(15, i * step_size, 5 - i), tex_id=2))
        # Cat
        add(Cat(app, pos=(0, -1, -10)))
        # Moving cube
        self.moving_cube = MovingCube(app, pos=(0, 6, 8), scale=(3, 1, 3), tex_id=1)
        add(self.moving_cube)

    def update(self):
        self.update_render_list()
        self.moving_cube.rot.xyz = self.app.time
