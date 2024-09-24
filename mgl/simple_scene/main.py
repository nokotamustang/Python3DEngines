import pygame
import moderngl
import sys

from core import Mesh, Light, SceneRenderer, Camera, Scene


class GraphicsEngine:
    # Options
    target_fps = 2000
    free_move = True
    vertical_sync = 0
    target_display = 0
    # Variables
    fps = 0
    time = 0
    delta_time = 0
    # State
    paused = False
    full_polygon = True
    full_screen = False

    def __init__(self, windowed_win_size=(1600, 900), full_screen_win_size=(1920, 1080)):
        # Initialize pygame modules
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        # Window size
        self.full_screen_win_size = full_screen_win_size
        self.windowed_win_size = windowed_win_size
        if self.full_screen:
            self.win_size = self.full_screen_win_size
        else:
            self.win_size = self.windowed_win_size
        # set OpenGL attributes
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, self.vertical_sync)
        # Create OpenGL context for 3D rendering
        self.game_screen = pygame.display.set_mode(self.win_size, flags=pygame.OPENGL | pygame.DOUBLEBUF,
                                                   display=self.target_display, vsync=self.vertical_sync)
        # Mouse settings
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        # Detect and use existing OpenGL context
        self.ctx = moderngl.create_context()
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
        self.ctx.gc_mode = 'auto'
        # Create an object to help track time
        self.clock = pygame.time.Clock()
        # Set fps max
        pygame.time.set_timer(pygame.USEREVENT, 1000 // self.target_fps)
        # light
        self.light = Light()
        # Camera
        self.camera = Camera(self)
        # Mesh
        self.mesh = Mesh(self)
        # Scene
        self.scene = Scene(self)
        # Renderer
        self.scene_renderer = SceneRenderer(self, self.scene)
        # Font
        self.font = pygame.font.SysFont('arial', 64)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                self.paused = not self.paused
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                self.full_polygon = not self.full_polygon
                self.toggle_full_polygon()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self.full_screen = not self.full_screen
                self.toggle_full_screen()

    def toggle_full_screen(self):
        if self.full_screen:
            self.win_size = self.full_screen_win_size
            pygame.display.set_mode(self.win_size, flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN,
                                    display=self.target_display, vsync=self.vertical_sync)
            self.ctx.viewport = (0, 0, *self.win_size)
            self.camera.set_aspect_and_projection()
        else:
            self.win_size = self.windowed_win_size
            pygame.display.set_mode(self.win_size, flags=pygame.OPENGL | pygame.DOUBLEBUF,
                                    display=self.target_display, vsync=self.vertical_sync)
            self.ctx.viewport = (0, 0, *self.win_size)
            self.camera.set_aspect_and_projection()

    def toggle_full_polygon(self):
        if self.full_polygon:
            self.ctx.wireframe = False
        else:
            self.ctx.wireframe = True

    def update(self):
        self.camera.update()
        self.scene_renderer.update()

    def render(self):
        # Clear frame buffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # Render scene
        self.scene_renderer.render()
        # Swap buffers
        pygame.display.flip()

    def run(self):
        while True:
            if not self.paused:
                self.time = pygame.time.get_ticks() * 0.001
            self.check_events()
            self.update()
            self.render()
            self.delta_time = self.clock.tick(self.target_fps)
            self.fps = self.clock.get_fps()
            print(f'fps: {self.fps:.2f} render_list: {len(self.scene_renderer.scene.render_list)}')


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
