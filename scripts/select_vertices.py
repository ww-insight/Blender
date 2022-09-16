import bpy
import math

bpy.ops.object.mode_set(mode='OBJECT')  # can change selection only in Object mode
# search for selected vertex
me = bpy.context.active_object.data
selected_vert = [v for v in bpy.context.active_object.data.vertices if v.select][0]


threshold_z_aprx = .10000
threshold_z = selected_vert.co.z
threshold_z_min = threshold_z - threshold_z_aprx
threshold_z_max = threshold_z + threshold_z_aprx
set_z_to = None


threshold_r_aprx  = .200
threshold_r_x = selected_vert.co.x
threshold_r_y = selected_vert.co.y

threshold_r = math.sqrt(threshold_r_x**2 + threshold_r_y**2)

threshold_r_min = threshold_r - threshold_r_aprx
threshold_r_max = threshold_r + threshold_r_aprx



# deselect all vertices
for face in me.polygons:  # you also have to deselect faces and edges
    face.select = False
for edge in me.edges:
    edge.select = False
for vert in me.vertices:
    vert.select = False
    # select vertices that are between thresholds
    if (threshold_z_min <= vert.co.z and vert.co.z <= threshold_z_max
        and threshold_r_min**2 < (vert.co.x**2 + vert.co.y**2) < threshold_r_max**2
    ):
        vert.select = True
        if set_z_to != None:
            vert.co.z = set_z_to
bpy.ops.object.mode_set(mode='EDIT') 
