from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionTraverser, CollisionNode, CollisionBox, CollisionSphere, CollisionRay, CollisionHandlerQueue
from panda3d.physics import ForceNode, LinearVectorForce, PhysicsCollisionHandler, PhysicsManager, PhysicsObject, AngularVectorForce, PhysicsCollisionHandler, ActorNode
from panda3d.core import ClockObject
from panda3d.core import DirectionalLight
from panda3d.core import AmbientLight
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties

import common
import math


block_size: int = 2
camera_swing_heading: int = 50
camera_swing_pitch: int = 50
camera_move_speed: int = 10
gravity: float = 9.81
jump_speed: float = 7
interaction_distance: int = 12
target_window_w, target_window_h = 1600, 900
target_window_w_half = target_window_w // 2
target_window_h_half = target_window_h // 2
mouse_border = 200

world_bounds_z = -8

start_z = 4

camera_width = 1
camera_radius = 2.0
soft_radius = 1.9
hard_radius = 1.75
soft_scaler = 0.5

frame_lock = 1 / 120


key_map = [
    {"key": "w", "action": "forward"},
    {"key": "s", "action": "backward"},
    {"key": "a", "action": "left"},
    {"key": "d", "action": "right"},
    {"key": "space", "action": "up"},
    {"key": "lcontrol", "action": "down"}
]


class Application(ShowBase):

    jump_velocity = 0
    place_block_type = 'grass'
    dt_counter = 0
    last_time = 0.0

    free_look = False

    def __init__(self):
        ShowBase.__init__(self)

        common.setup_window(self, target_window_w, target_window_h)
        common.load_models(self)
        common.load_images(self)

        common.add_sky_box(self, sky_box_name="blue")
        common.add_directional_light(self)
        common.add_ambient_light(self)

        self.generate_terrain()
        self.setup_fps_camera()
        self.setup_controls()

        # Add game update task to the task manager
        self.taskMgr.add(self.game_update, "update")

        # Add text to the screen
        self.setFrameRateMeter(True)  # Show FPS
        self.on_screen_status = common.add_text_object(self, text=f"block: {self.place_block_type}", pos=(-1.4, 0.9))
        self.on_screen_status = common.add_text_object(self, text=f"free_look: {self.free_look}", pos=(-1.4, 0.8))
        self.on_screen_keys_1 = common.add_text_object(self, text="1-4 : select block", pos=(0.9, 0.9))
        self.on_screen_keys_2 = common.add_text_object(self, text="wasd : movement", pos=(0.9, 0.8))
        self.on_screen_keys_3 = common.add_text_object(self, text="l-click, r-click : dig, place", pos=(0.9, 0.7))
        self.on_screen_keys_4 = common.add_text_object(self, text="f1 : toggle free look", pos=(0.9, 0.6))
        self.on_screen_keys_5 = common.add_text_object(self, text="space : jump", pos=(0.9, 0.5))
        self.on_screen_keys_6 = common.add_text_object(self, text="ctrl : down in free look", pos=(0.9, 0.4))

    def game_update(self, task):
        if task.time == 0.0:
            print("game update started")
            return task.cont
        self.last_time = task.time

        # dt = globalClock.getDt()  # The Panda3D way form the samples
        dt = ClockObject.getGlobalClock().getDt()  # Cleaner dt from the clock
        # dt = task.time - self.last_time  # Third way to get dt

        # Frame lock Testing
        # self.dt_counter += dt
        # if self.dt_counter < frame_lock:
        #     return task.cont
        # self.dt_counter -= frame_lock
        # dt = frame_lock

        # Movement
        x_movement = 0
        y_movement = 0
        z_movement = 0
        c_x = self.camera.getX()
        c_y = self.camera.getY()
        c_z = self.camera.getZ()
        c_h = math.radians(self.camera.getH())
        cos_c_h = math.cos(c_h)
        sin_c_h = math.sin(c_h)
        if self.key_state['forward']:
            x_movement -= dt * camera_move_speed * sin_c_h
            y_movement += dt * camera_move_speed * cos_c_h
        if self.key_state['backward']:
            x_movement += dt * camera_move_speed * sin_c_h
            y_movement -= dt * camera_move_speed * cos_c_h
        if self.key_state['left']:
            x_movement -= dt * camera_move_speed * cos_c_h
            y_movement -= dt * camera_move_speed * sin_c_h
        if self.key_state['right']:
            x_movement += dt * camera_move_speed * cos_c_h
            y_movement += dt * camera_move_speed * sin_c_h

        # Collision detection
        num_hits = 0
        if self.free_look == False and self.cTrav2 is not None:
            self.cTrav2.traverse(self.render)
            num_hits = self.camera_collision_queue.getNumEntries()
            hit_xyz = []
            if num_hits > 0:
                # self.camera_collision_queue.sortEntries()
                for i in range(num_hits):
                    hit = self.camera_collision_queue.getEntry(i)
                    hit_path = hit.getIntoNodePath()
                    hit_object = hit_path.getPythonTag('owner')
                    hit_block_position = hit_object.getPos()
                    hit_xyz.append(hit_block_position)
        # Gravity and Jump
        if self.free_look == False:
            if self.jump_velocity > 0:
                if num_hits > 0:
                    continue_jump = True
                    if continue_jump:
                        self.jump_velocity -= dt * gravity
                        z_movement += dt * self.jump_velocity
                        # print(f"jumping {round(self.jump_velocity, 2)}")
                else:
                    self.jump_velocity -= dt * gravity
                    z_movement += dt * self.jump_velocity
                    # print(f"jumping {round(self.jump_velocity, 2)}")
            elif self.key_state['up'] and self.jump_velocity == 0:
                self.jump_velocity = jump_speed
                # print(f"start jump {round(self.jump_velocity, 2)}")
            else:
                current_grid = self.camera.getPos() // block_size
                if current_grid.z < world_bounds_z:
                    self.camera.setZ(world_bounds_z)
                    self.jump_velocity = 0
                    c_x, c_y = 0, 0
                    c_z = start_z
                    # print(f"world bounds x{current_grid.x} y{current_grid.y} z{current_grid.z}")
                add_velocity = True
                if num_hits > 0:
                    for this_xyz in hit_xyz:
                        if this_xyz[2] <= c_z:
                            self.jump_velocity = 0
                            add_velocity = False
                            # print(f"hit ground {this_xyz[2]} <= {round(c_z, 2)}")
                            break
                if add_velocity:
                    self.jump_velocity -= dt * gravity
                    z_movement += dt * self.jump_velocity
        else:
            if self.key_state['up']:
                z_movement += dt * camera_move_speed
            if self.key_state['down']:
                z_movement -= dt * camera_move_speed

            # Soft and hard collision
        if num_hits > 0:
            for this_xyz in hit_xyz:
                collision_stop = False
                hit_delta_x = abs(c_x + x_movement - this_xyz[0])
                hit_delta_y = abs(c_y + y_movement - this_xyz[1])
                hit_delta_z = abs(c_z + z_movement - this_xyz[2])
                hit_delta_x2 = abs(c_x - this_xyz[0])
                hit_delta_y2 = abs(c_y - this_xyz[1])
                hit_delta_z2 = abs(c_z - this_xyz[2])
                hit_distance_x = math.sqrt(hit_delta_x ** 2 + hit_delta_y2 ** 2 + hit_delta_z2 ** 2)
                # if this_xyz[2] == c_z_block:
                if hit_distance_x <= soft_radius:
                    x_movement *= soft_scaler ** 2
                    y_movement *= soft_scaler
                    if self.jump_velocity > 0:
                        z_movement *= soft_scaler ** 2
                        self.jump_velocity -= dt * gravity
                    collision_stop = True
                    # print(f"soft x {round(hit_distance_x, 2)} < {soft_radius}")
                hit_distance_y = math.sqrt(hit_delta_x2 ** 2 + hit_delta_y ** 2 + hit_delta_z2 ** 2)
                if hit_distance_y <= soft_radius:
                    x_movement *= soft_scaler
                    y_movement *= soft_scaler ** 2
                    if self.jump_velocity > 0:
                        z_movement *= soft_scaler ** 2
                        self.jump_velocity -= dt * gravity
                    collision_stop = True
                    # print(f"soft y {round(hit_distance_y, 2)} < {soft_radius}")
                hit_distance_z = math.sqrt(hit_delta_x2 ** 2 + hit_delta_y2 ** 2 + hit_delta_z ** 2)
                if hit_distance_z <= soft_radius:
                    x_movement *= soft_scaler ** 2
                    y_movement *= soft_scaler ** 2
                    if self.jump_velocity > 0:
                        z_movement *= soft_scaler ** 2
                        self.jump_velocity -= dt * gravity
                    collision_stop = True
                    # print(f"soft z {round(hit_distance_z, 2)} < {soft_radius}")
                hit_distance = math.sqrt(hit_delta_x ** 2 + hit_delta_y ** 2 + hit_delta_z ** 2)
                if hit_distance <= hard_radius:
                    x_movement = 0
                    y_movement = 0
                    z_movement = 0
                    self.jump_velocity = 0
                    collision_stop = True
                    # print(f"hit xyx {round(hit_distance, 2)} < {hard_radius}")
                if collision_stop == True:
                    break

        self.camera.setPos(
            c_x + x_movement,
            c_y + y_movement,
            c_z + z_movement,
        )
        # print(f"x {x_movement} y {y_movement} z {z_movement} jump {self.jump_velocity}")

        # Look around
        mouse_pointer = self.mouseWatcherNode
        if mouse_pointer.hasMouse():
            mouse_x = mouse_pointer.getMouseX()
            mouse_y = mouse_pointer.getMouseY()
            # Mouse position is from -1 to 1, where 0 is the center
            # Convert to 0 to 1, where 0.5 is the center
            mouse_x = (mouse_x + 1) / 2
            mouse_y = (mouse_y + 1) / 2
            # Invert the Y axis
            mouse_y = 1 - mouse_y
            # Multiply by the window size to get the actual position
            mouse_x *= target_window_w
            mouse_y *= target_window_h
        else:
            mouse_x = 0
            mouse_y = 0
        if self.camera_active:
            now_h, now_p, _now_r = self.camera.getHpr()
            last_x = self.last_mouse_x
            last_y = self.last_mouse_y
            dx = (mouse_x - last_x)
            dy = (mouse_y - last_y)
            # Mouse will get locked to edge of window in Panda3D, so we need to move it back to the center to give
            # the appearance of free look, this also means we need an inside window border just incase the mouse moved
            # too far in one frame that it hits the edge of the window and we would lose information on how much it moved
            if mouse_x <= mouse_border:
                over_x = mouse_x - mouse_border
                mouse_x = target_window_w_half+over_x
                self.win.movePointer(0,  int(mouse_x), int(mouse_y))
            elif mouse_x >= target_window_w - mouse_border:
                over_x = mouse_x - (target_window_w - mouse_border)
                mouse_x = int(target_window_w_half+over_x)
                self.win.movePointer(0,  int(mouse_x), int(mouse_y))
            self.last_mouse_x = mouse_x
            if mouse_y <= mouse_border:
                over_y = mouse_y - mouse_border
                mouse_y = target_window_h_half+over_y
                self.win.movePointer(0,  int(mouse_x), int(mouse_y))
            elif mouse_y >= target_window_h - mouse_border:
                over_y = mouse_y - (target_window_h - mouse_border)
                mouse_y = int(target_window_h_half+over_y)
                self.win.movePointer(0,  int(mouse_x), int(mouse_y))
            self.last_mouse_y = mouse_y
            # Now we can move the camera with the mouse movement in dy and dx
            new_h = now_h - (dx * camera_swing_heading * dt)
            new_p = min(90, max(-90, now_p + (dy * -camera_swing_pitch * dt)))  # Lock pitch to -90 to 90 (up and down)
            self.camera.setHpr(new_h, new_p, 0)
            # print(f"x {last_x} y {last_y} h {new_h} p {new_p}")

        return task.cont

    def generate_terrain(self, size: tuple = (16, 16, 8)):
        last_z = size[2] - 1
        for z in range(size[2]):
            for x in range(size[0]):
                for y in range(size[1]):
                    if z == 0:
                        self.create_block(x * block_size - size[0], y * block_size - size[1], -z * block_size, "grass")
                    elif z == last_z:
                        self.create_block(x * block_size - size[0], y * block_size - size[1], -z * block_size, "stone")
                    else:
                        self.create_block(x * block_size - size[0], y * block_size - size[1], -z * block_size, "dirt")

    def setup_window(self):
        props = WindowProperties()
        props.setSize(target_window_w, target_window_h)
        self.win.requestProperties(props)

    def setup_fps_camera(self, position: tuple = (0, 0, start_z), look_at: tuple = (8, 0, 0)):
        self.disableMouse()  # Disable mouse control of the camera default
        self.camera.setPos(position)
        self.camLens.setFov(90)
        self.camLens.setNearFar(0.1, 1000)
        self.camera.lookAt(look_at)
        crosshair = self.images["crosshair"]
        crosshair.setScale(0.05)
        crosshair.setTransparency(TransparencyAttrib.MAlpha)
        # Setup collision detection for the camera line of sight
        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        ray_node = CollisionNode("camera_line_of_sight")
        ray_node.addSolid(ray)
        ray_node.setIntoCollideMask(0)
        ray_node_path = self.camera.attachNewNode(ray_node)
        self.ray_queue = CollisionHandlerQueue()
        self.cTrav.addCollider(ray_node_path, self.ray_queue)
        # self.cTrav.showCollisions(self.render)
        # Setup collision detection for below the camera for gravity using a CollisionSphere
        self.cTrav2 = CollisionTraverser()
        camera_collider_node = CollisionNode("camera_collision")
        camera_collider_node.addSolid(CollisionSphere(0, 0, 0, camera_radius))
        camera_collider = self.camera.attachNewNode(camera_collider_node)
        self.camera_collision_queue = CollisionHandlerQueue()
        self.cTrav2.addCollider(camera_collider, self.camera_collision_queue)
        # self.cTrav2.showCollisions(self.render)

    def capture_mouse(self):
        mouse_pointer = self.mouseWatcherNode
        if mouse_pointer.hasMouse():
            self.last_mouse_x = mouse_pointer.getMouseX()
            self.last_mouse_y = mouse_pointer.getMouseY()
            self.last_mouse_x = (self.last_mouse_x + 1) / 2
            self.last_mouse_y = (self.last_mouse_y + 1) / 2
            self.last_mouse_y = 1 - self.last_mouse_y
            # Multiply by the window size to get the actual position
            self.last_mouse_x *= target_window_w
            self.last_mouse_y *= target_window_h
        else:
            self.last_mouse_x = 0
            self.last_mouse_y = 0
        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)
        # properties.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(properties)
        self.camera_active = True

    def release_mouse(self):
        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)
        self.camera_active = False

    def change_key_state(self, key: str, value: bool):
        if key in self.key_state:
            self.key_state[key] = value

    def remove_block(self):
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            for i in range(self.ray_queue.getNumEntries()):
                ray_hit = self.ray_queue.getEntry(i)
                hit_path = ray_hit.getIntoNodePath()
                # normal = ray_hit.getSurfaceNormal(hit_path)
                hit_object = hit_path.getPythonTag('owner')
                if hit_object is not None:
                    distance_from_camera = hit_object.getDistance(self.camera)
                    if distance_from_camera < interaction_distance:
                        hit_path.clearPythonTag("owner")
                        hit_object.removeNode()
                    break

    def create_block(self, x: int, y: int, z: int, type: str):
        new_block = self.render.attachNewNode('block')
        new_block.setPos(x, y, z)
        if type == 'grass':
            self.models["grass"].instanceTo(new_block)
        elif type == 'dirt':
            self.models["dirt"].instanceTo(new_block)
        elif type == 'sand':
            self.models["sand"].instanceTo(new_block)
        elif type == 'stone':
            self.models["stone"].instanceTo(new_block)
        block_solid = CollisionBox((-1, -1, -1), (1, 1, 1))
        # block_solid = CollisionSphere(0, 0, 0, 1)
        block_node = CollisionNode(f'{x}_{y}_{z}')
        block_node.addSolid(block_solid)
        collider = new_block.attachNewNode(block_node)
        collider.setPythonTag('owner', new_block)

    def place_block(self):
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            c_x = self.camera.getX()
            c_y = self.camera.getY()
            c_z = self.camera.getZ()
            c_x_block = round(c_x / block_size) * block_size
            c_y_block = round(c_y / block_size) * block_size
            c_z_block = round(c_z / block_size) * block_size
            for i in range(self.ray_queue.getNumEntries()):
                ray_hit = self.ray_queue.getEntry(i)
                hit_path = ray_hit.getIntoNodePath()
                normal = ray_hit.getSurfaceNormal(hit_path)
                hit_object = hit_path.getPythonTag('owner')
                if hit_object is not None:
                    distance_from_camera = hit_object.getDistance(self.camera)
                    if distance_from_camera < interaction_distance:
                        hit_block_position = hit_object.getPos()
                        new_position = hit_block_position + normal * 2
                        delta_x = abs(c_x_block - new_position.x)
                        delta_y = abs(c_y_block - new_position.y)
                        delta_z = abs(c_z_block - new_position.z)
                        distance = math.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
                        if distance > camera_radius:
                            self.create_block(new_position.x, new_position.y, new_position.z, self.place_block_type)
                    break

    def place_test(self):
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            c_x = self.camera.getX()
            c_y = self.camera.getY()
            c_z = self.camera.getZ()
            c_x_block = round(c_x / block_size) * block_size
            c_y_block = round(c_y / block_size) * block_size
            c_z_block = round(c_z / block_size) * block_size
            for i in range(self.ray_queue.getNumEntries()):
                ray_hit = self.ray_queue.getEntry(i)
                hit_path = ray_hit.getIntoNodePath()
                normal = ray_hit.getSurfaceNormal(hit_path)
                hit_object = hit_path.getPythonTag('owner')
                if hit_object is not None:
                    distance_from_camera = hit_object.getDistance(self.camera)
                    if distance_from_camera < interaction_distance:
                        hit_block_position = hit_object.getPos()
                        new_position = hit_block_position + normal * 2
                        delta_x = abs(c_x_block - new_position.x)
                        delta_y = abs(c_y_block - new_position.y)
                        delta_z = abs(c_z_block - new_position.z)
                        distance = math.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
                        if distance > camera_radius:
                            print(f"test {distance}")
                    break

    def handle_mouse_click(self):
        self.capture_mouse()
        self.remove_block()

    def select_block_type(self, block_type: str):
        self.place_block_type = block_type
        self.on_screen_status.setText(f"block: {self.place_block_type}, free_look: {1 if self.free_look else 0}")
        print(f"selected block type: {block_type}")

    def toggle_free_look(self):
        self.free_look = not self.free_look
        self.on_screen_status.setText(f"block: {self.place_block_type}, free_look: {1 if self.free_look else 0}")
        print(f"free look: {self.free_look}")

    def setup_controls(self):
        self.key_state = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "jump": False,
            "up": False,
            "down": False
        }
        self.capture_mouse()
        self.accept("escape", self.release_mouse)
        self.accept("mouse1", self.handle_mouse_click)
        self.accept("mouse3", self.place_block)  # Right mouse button
        self.accept("mouse2", self.place_test)  # Middle mouse button
        self.accept("1", self.select_block_type, ["grass"])
        self.accept("2", self.select_block_type, ["dirt"])
        self.accept("3", self.select_block_type, ["sand"])
        self.accept("4", self.select_block_type, ["stone"])
        self.accept("f1", self.toggle_free_look)
        for key in key_map:
            self.accept(key["key"], self.change_key_state, [key["action"], True])
            self.accept(f"{key['key']}-up", self.change_key_state, [key["action"], False])


common.load_prc_file()
game = Application()
game.run()
