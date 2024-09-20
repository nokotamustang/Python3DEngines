# Python 3D Rendering Engines

An exploration of 3D engines and rendering in Python by `Nokota Mustang`.

All projects are working with Python 3.12.

## ./mgl - ModernGL and Pygame 3D demonstrations

To install use `pip install -r requirements.txt` to fetch the following packages:

-   moderngl==5.11.1
-   moderngl-window==2.4.6
-   pygame==2.6.0
-   PyGLM==2.7.1
-   numba==0.60.0
-   numpy==1.26.3
-   opensimplex==0.4.5.1
-   pywavefront==1.3.3

To run the example use `python main.py` from any of the project directories.

The basic example use ModernGL following this tutorial <https://www.youtube.com/watch?app=desktop&v=eJDIsFJN4OQ>. I've expanded on this adding more features, see below for the examples.

General keys:

-   `ESC` - Exit
-   `F1` - Pause time / Resume time
-   `F3` - View wire-frames
-   `WASD` - [Forward, Left, Backward, Right fly] camera movement

### ./mgl/cube/ - Cube with Lambert Diffusion & Blinn-Phong Specular lighting

![Screenshots](./screenshots/mgl_cube1.PNG)

We create a 3D cube from vertices, indices, and normals, and apply a simple lighting shader to it. We also have a first person camera with movement and controls using `WASD` and mouse for looking around.

### ./mgl/cubes/ - Cubes + textures

![Screenshots](./screenshots/mgl_cubes1.PNG)

Adding more cubes to the scene with texture mapping and multiple light sources.

### ./mgl/pbr/ - Physically based rendering (PBR)

![Screenshots](./screenshots/mgl_pbr1.PNG)

Using a PBR shader to render cubes with different materials and multiple light sources.

### ./mgl/grass/ - Grass rendering

Grass rendering using Geometry Shaders and bill boarding; and modelling wind movement using a flow map.

![Screenshots](./screenshots/mgl_grass1.PNG)

Starting from the tutorial: <https://vulpinii.github.io/tutorials/grass-modelisation/en/> and <https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass>.

Flow maps information and tools: <https://github.com/JaccomoLorenz/godot-flow-map-shader>

### ./mgl/ground/ - Ground rendering

Rendering a simple ground plane with a texture.

![Screenshots](./screenshots/mgl_ground1.PNG)

### ./mgl/water/ - Water rendering

Working on this example...

![Screenshots](./screenshots/mgl_water1.PNG)

### ./mgl/terrain/ - Complete terrain rendering

Rendering a ground plane from a height map. With terrain flora and water.

![Screenshots](./screenshots/mgl_terrain1.PNG)

Not ready yet...

### ./mgl/physics - Physics and collision detection

Working on this example...

### ./mgl/simple_scene/ - Combining simple features

![Screenshots](./screenshots/mgl_scene.PNG)

Textured cubes, shader programs, skybox, lighting and shadows. This is the same as the original example from the tutorial, but refactored and object culling added.

### ./mgl/sdf_ray_marching/ - SDF 'ray marching' rendering

![Screenshots](./screenshots/mgl_sdf.PNG)

Following the tutorials: <https://www.youtube.com/watch?v=hUaYxqkrfjA> and <https://www.youtube.com/watch?v=i12pFwXlOGw>.

We build a simple scene using Signed Distance Functions (SDF) to render a sphere and building around it. The example extends to use AA, shadows, reflections, and bump mapping.

### More Features To Add

Wish list includes:

-   Global and local illumination shapes
-   More model types (blender, gltf, etc)
-   Skeletal animation
-   Draw text to the screen
-   Reflections and refractions
-   Post Processing
-   Anti-aliasing

## ./p3d - Panda3D demonstrations

My first test in **Panda3D** following the basic tutorial for minecraft style block rendering from <https://www.youtube.com/watch?v=xV3gH1JZew4>.

![Screenshots](./screenshots/panda_1.PNG)

We load in textured block meshes from **.glb** model files, create a simple grid, add a skybox, and have simple camera with movement and controls to dig or place blocks with Ray collision detection.

I added better camera controls and some collision detection for the 'camera' player in my example.

To install use `pip install -r requirements.txt` to fetch the following packages:

-   panda3d==1.10.14
-   types-panda3d==0.4.1
-   panda3d-gltf==1.1.0

To run the example use `python main.py` from any of the project directories.

I have halted for now to work on ModernGL instead.
