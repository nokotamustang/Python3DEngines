# Python 3D Rendering Engines

An exploration of 3D engines and rendering in Python by `Nokota Mustang`.

All projects are working with Python 3.12.

## ursina - Ursina 3D engine

Will be exploring the Ursina 3D engine soon, nothing here yet...

## mgl - ModernGL and Pygame 3D demonstrations

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

The basic example use ModernGL following this tutorial from 'Coder Space': <https://www.youtube.com/watch?app=desktop&v=eJDIsFJN4OQ>. I've expanded on this adding more features, see below for the examples.

General keys in the examples:

-   `ESC` - Exit
-   `F1` - Pause time / Resume time
-   `F3` - Toggle view of wire-frames
-   `F11` - Toggle full screen
-   `WASD` - [Forward, Left, Backward, Right fly] camera movement

### mgl/cube - Cube with Lambert Diffusion & Blinn-Phong Specular lighting

We create a 3D cube from vertices, indices, and normals, and apply a simple lighting shader to it.

![Screenshots](./screenshots/mgl_cube1.PNG)

### mgl/cubes - Cubes + textures

Adding more cubes to the scene with texture mapping and multiple light sources.

![Screenshots](./screenshots/mgl_cubes1.PNG)

### mgl/cubes_2 - Cubes + textures + shadows

Added shadows to the cubes demo; this example also re-uses shaders and therefore shader program values are set for each object before rendering.

![Screenshots](./screenshots/mgl_cubes2.PNG)

In an ideal situation, we would send all data in matrices to the shader, and then render all objects in one go with minimal value changes to the shader program.

Additionally, this uses a single shadow map for all objects in the scene i.e. only one light direction is modelled. Some changes are needed to support shadows from multiple light sources. If I code that, I will be adding global lighting as well.

### mgl/simple_scene - Combining simple features

Complete example from 'Coder Space' tutorial.

![Screenshots](./screenshots/mgl_scene.PNG)

Using textured cubes, shader programs, skybox, lighting and shadows. This is the same as the original example from the tutorial, but refactored and I've added some object culling.

### mgl/pbr - Physically based rendering (PBR)

Using a PBR shader to render cubes with different materials and multiple light sources.

![Screenshots](./screenshots/mgl_pbr1.PNG)

### mgl/grass - Grass rendering

Grass rendering using Geometry Shaders and bill boarding; and modelling wind movement using a flow map.

![Screenshots](./screenshots/mgl_grass1.PNG)

Starting from the tutorial: <https://vulpinii.github.io/tutorials/grass-modelisation/en/> and <https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass>.

Flow maps information and tools: <https://github.com/JaccomoLorenz/godot-flow-map-shader>

### mgl/grass_2 - Grass rendering from a texture atlas

Expanding on the grass rendering to use a texture atlas for the grass models.

![Screenshots](./screenshots/mgl_grass2.PNG)

_Just indexing manually right now in the geom shader; so I will add controls to select the grass type or I will extend to paint different grass types on the ground._

### mgl/ground - Ground rendering

Rendering a simple ground plane with a texture.

![Screenshots](./screenshots/mgl_ground1.PNG)

### mgl/ground_2 - Ground rendering with a 'height map'

Rendering a simple ground plane with a texture and a height map.

![Screenshots](./screenshots/mgl_ground2.PNG)

### mgl/ground_3 - Ground and grass rendering

I've combined several techniques to render the ground plane with a height map, and calculating normals for lighting. The grass is placed on the triangles of the ground plane, and the grass is affected by the height map.

![Screenshots](./screenshots/mgl_ground3.PNG)

I added a global lighting model, and adding our local lights to the scene; and added a skybox.

### mgl/ground_4 - Chunks + dynamic loading

<!-- Obviously the ground_3 demo is slow with a large height map, so I've added a chunk system to load and unload parts of the height map as the camera moves around. -->

<!-- ![Screenshots](./screenshots/mgl_ground4.PNG) -->

Not ready yet...

### mgl/water - Water rendering

Not ready yet...

### mgl/physics - Physics and collision detection

Not ready yet...

### mgl/aa - Anti-aliasing

Not ready yet...

### mgl/terrain - Complete terrain rendering with editor tools

Not ready yet...

### mgl/sdf_ray_marching - SDF 'ray marching' rendering

Following the tutorials: <https://www.youtube.com/watch?v=hUaYxqkrfjA> and <https://www.youtube.com/watch?v=i12pFwXlOGw>.

![Screenshots](./screenshots/mgl_sdf.PNG)

We build a simple scene using Signed Distance Functions (SDF) to render a sphere and building around it. The example extends to use AA, shadows, reflections, and bump mapping.

### More Features To Add

Wish list for much later down the road includes the following:

-   Global and local illumination shapes
-   More model types (blender, gltf, etc)
-   Skeletal animation
-   Draw text to the screen
-   Reflections and refractions
-   Post Processing

## p3d - Panda3D demonstrations

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
