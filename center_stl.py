import bpy

min_z = max_z = None
min_x = max_x = None
min_y = max_y = None

# deselect all vertices
bpy.ops.object.mode_set(mode='OBJECT')  # can change selection only in Object mode
me = bpy.context.active_object.data
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
bpy.context.active_object.location = [0,0,0]

for face in me.polygons:  # you also have to deselect faces and edges
    face.select = False
for edge in me.edges:
    edge.select = False
for vert in me.vertices:
    edge.select = False
    #search for the most lower vertice
    if min_z == None or vert.co.z < min_z:
        min_z = vert.co.z
    if max_z == None or vert.co.z > max_z:
        max_z = vert.co.z        
        
for vert in me.vertices:
    if vert.co.z == min_z:
        vert.select = True
        if min_x == None or vert.co.x < min_x:
            min_x = vert.co.x
        if max_x == None or vert.co.x > max_x:
            max_x = vert.co.x
        if min_y == None or vert.co.y < min_y:
            min_y = vert.co.y
        if max_y == None or vert.co.y > max_y:
            max_y = vert.co.y    

#bpy.context.active_object.location[0] -= min_x - (max_x + min_x)/2
#bpy.context.active_object.location[1] -= min_y - (max_y + min_y)/2
bpy.context.active_object.location[0] += bpy.context.active_object.location[0] - min_x - (max_x - min_x)/2
bpy.context.active_object.location[1] += bpy.context.active_object.location[1] - min_y - (max_y - min_y)/2
bpy.context.active_object.location[2] -= min_z 
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
# enter edit mode and delete vertices
bpy.ops.object.mode_set(mode='EDIT')
