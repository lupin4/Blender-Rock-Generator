import bpy
import random


def clean_scene():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
        
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)
        
    



def make_noise(intensity = 0.2, scale = 0.86):
    bpy.ops.texture.new()
    texture = bpy.data.textures["Texture"]
    texture.type = 'VORONOI'
    bpy.data.textures["Texture"].distance_metric = 'DISTANCE_SQUARED'
    bpy.data.textures["Texture"].noise_intensity = intensity
    bpy.data.textures["Texture"].noise_scale = scale
    return texture

#    bpy.context.active_object.modifiers[-1].texture = texture

    
    


def create_cube():
    bpy.ops.mesh.primitive_cube_add()
    return bpy.context.object

def subdivide(obj, name, levels):
    modifier = obj.modifiers.new(type="SUBSURF", name = name)
    modifier.levels = levels
    

def displace(obj):
    bpy.ops.object.modifier_add(type='DISPLACE')
    texture = make_noise(
        intensity = random.uniform(0.1, 0.4),
        scale = random.uniform(0.7, 1.3)
    )

    bpy.context.active_object.modifiers[-1].texture = texture
    
    
def decimate(obj, ratio):
    modifier = bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = ratio    


def get_vert_offset(vertex, scale):
    # Calculate a random direction based on the normal
    offset_direction = vertex.normal.copy()
    offset_direction.x += random.uniform(-0.5, 0.5)
    offset_direction.y += random.uniform(-0.5, 0.5)
    offset_direction.z += random.uniform(-0.5, 0.5)
    offset_direction.normalize()  # Normalize to ensure it's a unit vector
    return offset_direction * scale

def offset_verts(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch to object mode to manipulate vertices

    for vertex in obj.data.vertices:
        offset = get_vert_offset(vertex, 2)
        vertex.co += offset  # Apply the calculated offset to the vertex position

      
    
    
def collapse_modifiers(obj):
    for modifier in obj.modifiers:
        print(modifier)
        # Apply modifiers by name
        if obj.modifiers.get("Subdivide"):
            bpy.ops.object.modifier_apply(modifier="Subdivide")
        if obj.modifiers.get("Displace"):
            bpy.ops.object.modifier_apply(modifier="Displace")
        if obj.modifiers.get("Decimate"):
            bpy.ops.object.modifier_apply(modifier="Decimate")


def make_rock():
    
    cube = create_cube()
    subdivide(cube, name= "Subdivide", levels=5)
    print(dir(cube))
    displace(cube)
    decimate(cube, ratio = 0.1)
    offset_verts(cube)
    print('we will create a rock')
    
    collapse_modifiers(cube)


  
clean_scene()
make_rock()