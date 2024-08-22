from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import loadPrcFile
from panda3d.core import DirectionalLight
from panda3d.core import AmbientLight
from panda3d.core import WindowProperties
from direct.gui.OnscreenText import OnscreenText, TextNode
import os

settings_file = "settings.prc"
asset_dir = "asset"
full_model_dir = f"{asset_dir}/model"
full_sky_box_dir = f"{asset_dir}/sky_box"
full_image_dir = f"{asset_dir}/image"


def load_prc_file():
    loadPrcFile(settings_file)


def get_files_in_dir(dir_to_scan: str, extension: str = ".pdf", get_just_name: bool = False) -> list:
    '''Get all the files in a directory.
    Args:
        dir_to_scan (str): The directory to scan.
        file_end_type (str): The file end type.
        get_just_name (bool): Whether to get just the name of the file. Defaults to False.
    Returns:
        list: The list of files.
    '''
    all_files = []
    raw_list = os.listdir(dir_to_scan)
    if extension is not None:
        extension = extension.lower()
        if get_just_name == True:
            for file_name in os.listdir(dir_to_scan):
                if file_name.lower().endswith(extension):
                    all_files.append(os.path.splitext(file_name)[0])
        else:
            for file_name in raw_list:
                if file_name.lower().endswith(extension):
                    all_files.append(f"{dir_to_scan}/{file_name}")
    else:
        all_files = raw_list
    return all_files


def setup_window(self: ShowBase, target_window_w: int, target_window_h: int) -> None:
    '''Setup window properties
    Args:
        target_window_w (int): Target window width
        target_window_h (int): Target window height
    '''
    props = WindowProperties()
    props.setSize(target_window_w, target_window_h)
    self.win.requestProperties(props)
    self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)


def load_models(self: ShowBase, model_dir: str = None, model_type: str = "glb") -> None:
    '''Load models from the specified directory
    Args:
        model_dir (str): Directory to load models from
        model_type (str): Model file type
    '''
    self.models = {}
    if model_dir is None:
        source_path = full_model_dir
    else:
        source_path = model_dir
    files = get_files_in_dir(source_path, model_type)
    for file in files:
        model = self.loader.loadModel(file)
        model_name = os.path.splitext(os.path.basename(file))[0]
        self.models[model_name] = model
        print(f"loaded model: {model_name}")


def load_images(self: ShowBase, image_dir: str = None, image_type: str = "png", image_scale: float = 1.0) -> None:
    '''Load images from the specified directory
    Args:
        image_dir (str): Directory to load images from
        image_type (str): Image file type
        image_scale (float): Scale of the
    '''
    self.images = {}
    if image_dir is None:
        source_path = full_image_dir
    else:
        source_path = image_dir
    files = get_files_in_dir(source_path, image_type)
    for file in files:
        image = OnscreenImage(image=file, pos=(0, 0, 0), scale=image_scale)
        image_name = os.path.splitext(os.path.basename(file))[0]
        self.images[image_name] = image
        print(f"loaded image: {image_name}")


def add_directional_light(self: ShowBase, direction: tuple = (0, -60, 0), color: tuple = (1, 1, 1, 1), shadow: bool = True) -> None:
    '''Add a directional light to the scene
    Args:
        direction (tuple): Direction of the light
        color (tuple): Color of the light
        shadow (bool): Enable shadow
    '''
    light = DirectionalLight("directional_light")  # Create a directional light
    light.setColor(color)  # Set the color of the light
    light.setShadowCaster(shadow, 512, 512)  # Enable shadows
    light_node_path = self.render.attachNewNode(light)  # Create a NodePath and attach the light to its
    light_node_path.setHpr(direction)  # Set the direction of the light in Heading, Pitch, Roll
    self.render.setLight(light_node_path)  # Set the light to render
    print(f"added directional light: {direction}")


def add_ambient_light(self: ShowBase, color: tuple = (0.25, 0.25, 0.25, 1)) -> None:
    '''Add an ambient light to the scene
    Args:
        color (tuple): Color of the light
    '''
    light = AmbientLight("ambient_light")  # Create an ambient light
    light.setColor(color)  # Set the color of the light
    light_node_path = self.render.attachNewNode(light)  # Create a NodePath and attach the light to its node
    self.render.setLight(light_node_path)  # Set the light to render
    print(f"added ambient light: {color}")


def add_sky_box(self: ShowBase, size: int = 500, position: tuple = (0, 0, 0), sky_box_dir: str = None, sky_box_name: str = "blue", sky_box_ext: str = "egg") -> None:
    '''Add a sky box to the scene
    Args:
        size (int): Size of the sky box
        position (tuple): Position of the sky box
        sky_box_dir (str): Directory of the sky box
        sky_box_name (str): Name of the sky box
        sky_box_ext (str): Extension of the sky box
    '''
    if sky_box_dir is None:
        source_path = full_sky_box_dir
    else:
        source_path = sky_box_dir
    sky_box = self.loader.loadModel(f"{source_path}/{sky_box_name}.{sky_box_ext}")
    sky_box.setScale(size)
    sky_box.setBin("background", 1)  # Set the render order of the sky box to be rendered before everything beyond it
    sky_box.setDepthWrite(0)  # Disable writing to the depth buffer
    sky_box.setLightOff()  # Disable lighting
    sky_box.setPos(position)
    sky_box.reparentTo(self.render)
    print(f"loaded sky box: {sky_box_name}")


def add_text_object(self: ShowBase, text: str, pos: tuple = (0, 0), scale: float = 0.05, color: tuple = (1, 1, 1, 1), may_change: bool = True) -> OnscreenText:
    '''Add text object to the scene
    Args:
        text (str): Text to display
        pos (tuple): Position of the text object
        scale (float): Scale of the text object
        color (tuple): Color of the text object
        align (str): Alignment of the text object
        may_change (bool): Allow the text to change, False for static text with better performance
    Returns:
        text_object (OnscreenText): Text object
    '''
    text_object = OnscreenText(text=text, pos=pos, scale=scale, fg=color, align=TextNode.ALeft, mayChange=may_change)
    return text_object
