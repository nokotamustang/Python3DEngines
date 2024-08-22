import pygame
import moderngl
import sys
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer


class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)):
        # init pygame modules
        pygame.init()
        # window size
        self.WIN_SIZE = win_size
        # set OpenGL attr
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        # create OpenGL context
        pygame.display.set_mode(self.WIN_SIZE, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        # mouse settings
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        # detect and use existing OpenGL context
        self.ctx = moderngl.create_context()
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        # create an object to help track time
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0
        # light
        self.light = Light()
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)
        # renderer
        self.scene_renderer = SceneRenderer(self)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pygame.quit()
                sys.exit()

    def render(self):
        # clear frame buffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene_renderer.render()
        # swap buffers
        pygame.display.flip()

    def get_time(self):
        self.time = pygame.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
