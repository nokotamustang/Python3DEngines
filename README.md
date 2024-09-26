# Python 3D Rendering Engines

An exploration of 3D engines and rendering in Python by `Nokota Mustang`.

Computer graphics is a vast field, and I am interested in learning more about the rendering process and the mathematics behind it. Having a good grasp of realtime graphics, data structures, and algorithms is essential for game development, simulations, and visualizations. I've completed 2D game projects before, but I want to learn more about 3D graphics and rendering.

There is a lot of crossover to modern App development, and the skills learned here can be applied to AR/VR, simulations, and data visualization. In addition data processing and machine learning can benefit from the parallel processing capabilities of the GPU; so learning about graphics rendering is a good investment of time.

Opengl is a low-level graphics API that can be used to create 3D graphics, but it is quite complex and requires a lot of boilerplate code to get started. ModernGL is a Python wrapper around OpenGL that simplifies the process of creating 3D graphics.

There are several very large and detail books about graphics rendering, but when it comes to creating real-time graphics with interactive applications, there is a complex balance between performance and quality.

This means there are several ideas and solutions to some of the same problems, but the issue becomes how to combine multiple techniques to create a coherent and efficient system.

In the case if Disney's Panda3D, it is a game engine that simplifies the process of creating 3D games with c++ or Python. However usually when exploring a game engine, the low level rendering process is abstracted away, and an assortment of tools and features are provided, which also sometimes carries code-bloat and performance overhead. The bigger the engine, the more features and tools are available, but the more complex and harder to learn it becomes; such in the case of Unity or Unreal Engine 4 or 5.

Therefore to learn how to approach graphics from a first-principles perspective, I will be exploring Python based rendering engines. Why Python? Because it is a high-level language that is easy to learn and use, and it is also a language that I am familiar with and it's one of the most powerful and popular tools out there today. I also have a series that will explore c++ with Vulkan, but that is a different story.

How to use this repository? Each project is a standalone example of a 3D rendering technique or feature. Some projects are combined to create a more complex scene. Each project is a self-contained example that can be run independently. All projects are working with Python 3.12.

## mgl - ModernGL and Pygame 3D demonstrations

ModernGL wraps OpenGL in Python and simplifies the process of creating 3D graphics. Pygame is a set of Python modules designed for writing video games. It includes computer graphics and sound libraries designed to be used with the Python programming language. This makes a perfect pair of libraries to create 3D graphics in Python. I will build a series of examples using ModernGL and Pygame to explore 3D rendering techniques, and eventually combine them to create a 3D game engine.

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

General keys in the examples:

-   `ESC` - Exit
-   `F1` - Pause time / Resume time
-   `F3` - Toggle view of wire-frames
-   `F11` - Toggle full screen
-   `WASD` - [Forward, Left, Backward, Right fly] camera movement

### mgl/cube - Cube with Lambert Diffusion & Blinn-Phong Specular lighting

Create a 3D cube from vertices, indices, and normals, and apply a simple lighting shader to it.

![Screenshots](./screenshots/mgl_cube1.PNG)

This is a basic example creating a 3D mesh from scratch and applying a simple shader program to it. The shader program is a combination of Lambert Diffusion and Blinn-Phong Specular lighting models.

Because we communicate with the GPU using OpenGL under the hood, we need to send data to the GPU in the form of buffers. We create a Vertex Buffer Object (VBO) to store the vertices, and an Element Buffer Object (EBO) to store the indices of the vertices that make up the triangles of the cube.

The shader program is a combination of a vertex shader and a fragment shader. The vertex shader is responsible for transforming the vertices of the cube into screen space, and the fragment shader is responsible for calculating the color of each pixel on the cube. These shaders are written in GLSL (OpenGL Shading Language) and operate in parallel on the GPU via thousands shader cores.

Therefore learning to write code in parallel is essential for creating efficient graphics applications.

### mgl/cube_2 - Anti-aliasing

Added anti-aliasing with a sized up render buffer with 4 samples.

![Screenshots](./screenshots/mgl_cube2.PNG)

The basic principle of anti-aliasing is to render the scene at a higher resolution and then down-sample it to the screen resolution. This is done by rendering the scene to a render buffer with a higher resolution than the screen, and then down-sampling it to the screen resolution using a shader program.

Without anti-aliasing, the edges of the cube appear jagged because the pixels on the screen are square and the edges of the cube are not aligned with the pixels. Anti-aliasing smooths out the edges of the cube by blending the colors of the pixels along the edges.

### mgl/cubes - Cubes + textures

Adding more cubes to the scene with texture mapping and multiple light sources.

![Screenshots](./screenshots/mgl_cubes1.PNG)

This example adds more cubes to the scene and applies a texture to each cube. The texture is a 2D image that is mapped to the surface of the cube using texture coordinates. The texture coordinates are stored in the VBO along with the vertices of the cube.

With basic illumination applied in addition to the texture the scene is starting to look more realistic. The floor is a grid of cubes to illustrate how to create a large scene with many objects. However, this is usually considered inefficient because each cube is a separate draw call to the GPU; whereas for a floor only the top faces of the cubes are visible. More on this later.

### mgl/cubes_2 - Cubes + textures + shadows

Added shadows to the cubes demo; this example also re-uses shaders and therefore shader program values are set for each object before rendering.

![Screenshots](./screenshots/mgl_cubes2.PNG)

The shadows are created using a shadow map. A shadow map is a depth buffer that is rendered from the perspective of the light source. The depth buffer is then used to determine if a pixel on the cube is in shadow or not. If the pixel is in shadow, it is darkened; if it is not in shadow, it is illuminated.

OpenGL is efficient and has some tools that compute some of these factors on the GPU, and we can use the shader program to calculate the state of a pixel, whether it is in shadow or not.

In an ideal situation, we would send all data in matrices to the shader, and then render all objects in one go with minimal value changes to the shader program.

Additionally, this uses a single shadow map for all objects in the scene i.e. only one light direction is modelled. Some changes are needed to support shadows from multiple light sources.

### mgl/simple_scene - Combining simple features

The basic example use ModernGL following this tutorial from 'Coder Space': <https://www.youtube.com/watch?app=desktop&v=eJDIsFJN4OQ>. I've expanded on this adding more features, see below for the examples.

![Screenshots](./screenshots/mgl_scene.PNG)

Using textured cubes, shader programs, skybox, lighting and shadows. This is the same as the original example from the tutorial, but refactored and I've added some object culling.

### mgl/pbr - Physically based rendering (PBR)

Using a PBR shader to render cubes with different materials and multiple light sources.

![Screenshots](./screenshots/mgl_pbr1.PNG)

PBR is a rendering technique that simulates the way light interacts with materials in the real world. It is based on the physics of light and materials, and it is used to create realistic lighting and shading effects in 3D graphics.

The basic idea behind PBR is to use physically accurate models to simulate the way light interacts with materials. This includes models for diffuse reflection, specular reflection, and transmission. These models are based on the physical properties of materials, such as their reflectance, roughness, and index of refraction.

Therefore each material has a set of properties that describe how it interacts with light. These properties include the albedo, roughness, metallic, and normal map. The albedo is the base color of the material, the roughness is how rough or smooth the material is, the metallic is how metallic or non-metallic the material is, and the normal map is a texture that simulates surface detail.

We can assign these properties to each cube in the scene, and then use a PBR shader to render the cubes with realistic lighting and shading effects. The PBR shader uses the properties of the material to calculate the color of each pixel on the cube, with the properties of the light sources in the scene and produces a more realistic effect as the light interacts with the material.

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

Rendering a simple ground plane with a texture and a height map from an image.

![Screenshots](./screenshots/mgl_ground2.PNG)

### mgl/ground_3 - Ground and grass rendering

I've combined several techniques to render the ground plane with a height map, and calculating normals for lighting.

The grass is placed on the triangles of the ground plane, and so the grass moves with the ground heights.

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

### mgl/terrain - Complete terrain rendering

<!-- Combining ground, grass, and water rendering to create a complete terrain scene; with shadows, skybox, and illumination. -->

Not ready yet...

### mgl/sdf_ray_marching - SDF 'ray marching' rendering

Following the tutorials: <https://www.youtube.com/watch?v=hUaYxqkrfjA> and <https://www.youtube.com/watch?v=i12pFwXlOGw>.

![Screenshots](./screenshots/mgl_sdf.PNG)

Building a simple scene using Signed Distance Functions (SDF) to render a sphere and building around it. The example extends to use AA, shadows, reflections, and bump mapping. Everything is contained in shader programs!

<!-- ### More Features To Add

Wish list for much later down the road includes the following:

-   Global and local illumination shapes
-   More model types (blender, gltf, etc)
-   Skeletal animation
-   Draw text to the screen
-   Reflections and refractions
-   Post Processing -->

## p3d - Panda3D demonstrations

My first test in **Panda3D** following the basic tutorial for minecraft style block rendering from <https://www.youtube.com/watch?v=xV3gH1JZew4>.

![Screenshots](./screenshots/panda_1.PNG)

Load in textured block meshes from **.glb** model files, create a simple grid, add a skybox, and have simple camera with movement and controls to dig or place blocks with Ray collision detection.

I added better camera controls and some collision detection for the 'camera' player in my example.

To install use `pip install -r requirements.txt` to fetch the following packages:

-   panda3d==1.10.14
-   types-panda3d==0.4.1
-   panda3d-gltf==1.1.0

To run the example use `python main.py` from any of the project directories.

I have halted for now to work on ModernGL instead.

## ursina - Ursina 3D engine

Will be exploring the Ursina 3D engine soon, nothing here yet...
