import bpy
import sys
import math
import numpy as np

# Constants
PI = math.pi
D2R = PI/180.

# Settings
width = 800
height = 800
z_height = 0.25 # Displace modifier strength
tex_res = 1     # Texture resolution (1:1)
mesh_res = 4    # Mesh resolution (8:1)

# Change to return data (should be between 0-1)
scale = 20
def get_data(x, y, frame, fps):
    x -= width/2
    y -= height/2
    
    x /= scale
    y /= scale
    
    time = frame/fps

    period = 2
    phimin = 0
    phimax = 2*PI
    phi = (time/period)*(phimax - phimin)
    
    r = math.sqrt(x**2+y**2)
    return (math.sin(r - phi) + 0.3*math.sin(x - 2*phi) + 0.15*math.sin(y - 4*phi) + 1.45)/2.9

# Change to get color (you can use the ones defined below)
def get_color(x, y, frame, fps):
    a = get_data(x, y, frame, fps)
    return lerp(a, (1, 0, 0), (0, 0, 1))
    
    
# Color maps:

## One color map (from dark to light)
def one_color(a, c):
    return lerp_n(
        a, [(0, 0, 0), c, (1, 1, 1)]
    )
    
# Linear interpolation between two colors
def lerp(a, c1, c2):
    return (
        (1-a)*c1[0] + a*c2[0],
        (1-a)*c1[1] + a*c2[1],
        (1-a)*c1[2] + a*c2[2]
    )

# Linear interpolation between n_colors
def lerp_n(a, colors):
    if a == 1: return colors[-1]
    n = len(colors) - 1
    s = math.floor(a*n)
    b = a*n - s
    return lerp(b, colors[s], colors[s+1])
    
# Rainbow colors
def rainbow(a):
    return lerp_n(
            a,
            [
                (1, 0, 0), # red
                (1, 1, 0), # yellow
                (0, 1, 0), # green
                (0, 1, 1), # cyan
                (0, 0, 1), # blue
                (1, 0, 1)  # magenta
            ]
        )

def main():
    
    # Evaluate command line options
    frame = int(sys.argv[10])
    tot_frames = int(sys.argv[11])
    seconds = float(sys.argv[12])
    
    fps = tot_frames/seconds
    
    # Variables
    mesh_width = int(width/mesh_res)
    mesh_height = int(height/mesh_res)
    tex_width = int(width/tex_res)
    tex_height = int(height/tex_res)
    size = 2
    aspect_ratio = width/height

    # Delete Cube
    bpy.ops.object.delete(use_global=False, confirm=False)
    
    # Position Camera
    camera = bpy.data.objects['Camera']
    camera.location = [3.44, -1.83, 2.37]
    camera.rotation_euler = np.array([56.2, 0., 61.5])*D2R
    
    # Set background lighting to zero
    world = bpy.data.worlds["World"]
    world.node_tree.nodes["Background"].inputs[1].default_value = 0

    # Create and name a grid
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=mesh_width, y_subdivisions=mesh_height ,size=size, location=(0, 0, 0))

    plotObject = bpy.context.active_object
    plotObject.name = 'Surface_Plot'

    # Size grid  properly
    plotObject.scale[0] = aspect_ratio
    plotObject.scale[1] = 1

    # Generate a displace and diffuse map
    displace_image = bpy.data.images.new("Displace_Map", width=tex_width, height=tex_height)
    diffuse_image = bpy.data.images.new("Diffuse_Map", width=tex_width, height=tex_height)

    displace_pixels = [None] * tex_width * tex_height
    diffuse_pixels = [None] * tex_width * tex_height


    for x in range(tex_width) :
        for y in range(tex_height) :
            a = get_data(x, y, frame, fps)
            displace_pixels[(y * tex_width) + x] = [a, a, a, 1.0]

            r, g, b = get_color(x, y, frame, fps)
            diffuse_pixels[(y * tex_width) + x] = [r, g, b, 1.0]

    displace_pixels = [chan for px in displace_pixels for chan in px]
    diffuse_pixels = [chan for px in diffuse_pixels for chan in px]

    displace_image.pixels = displace_pixels
    diffuse_image.pixels = diffuse_pixels
            
    displace_image.filepath_raw = '//img/Displace_Map.png'
    displace_image.file_format = 'PNG'
    displace_image.save()

    diffuse_image.filepath_raw = '//img/Diffuse_Map.png'
    diffuse_image.file_format = 'PNG'
    diffuse_image.save()

    # Create a displace texture
    displace_map = bpy.data.textures.new('Displace_Texture', type='IMAGE')
    displace_map.image = displace_image

    # Create a displace modifier
    plotObject.modifiers.clear()
    displace_mod = plotObject.modifiers.new("Displace", type='DISPLACE')
    displace_mod.texture = displace_map
    displace_mod.strength = z_height

    # Create a material
    material = bpy.data.materials.new(name="Plot_Material")
    # Use nodes
    material.use_nodes = True
    # Add Principled BSDF
    bsdf = material.node_tree.nodes["Principled BSDF"]
    # Add an ImageTexture
    diffuse_map = material.node_tree.nodes.new('ShaderNodeTexImage')
    # Set diffuse image
    diffuse_map.image = diffuse_image
    # Link ImageTexture to Principled BSDF
    material.node_tree.links.new(bsdf.inputs['Base Color'], diffuse_map.outputs['Color'])

    # Assign it to object
    if plotObject.data.materials :
        plotObject.data.materials[0] = material
    else :
        plotObject.data.materials.append(material)

    # Shade smooth
    mesh = bpy.context.active_object.data
    for f in mesh.polygons :
        f.use_smooth = True
        
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "OPTIX"
    bpy.context.scene.cycles.device = 'GPU'

    # bpy.ops.wm.save_as_mainfile(filepath="/home/philip/BlenderModels/4DPlot/4Dplot.blend")

if __name__ == "__main__" :
    main()
