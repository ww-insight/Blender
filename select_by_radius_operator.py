import bpy
import math
from bpy.props import *

class SelectByRadiusOperator(bpy.types.Operator):
    """Select vertices by circle radius from selecter vertex"""
    bl_idname = "object.select_by_radius"
    bl_label = "Select by radius Operator"
    bl_options = {'REGISTER', 'UNDO'}
    
    # create props
    thrs_z_offset_min : FloatProperty(name = "Offset Z min", description = "Selecting vertices lower current by", default = .10000, min = 0)
    thrs_z_offset_max : FloatProperty(name = "Offset Z max", description = "Selecting vertices highier current by", default = .10000, min = 0)   
    thrs_r_offset_min : FloatProperty(name = "Offset R min", description = "Offset for radius", default = .10000, min = 0)
    thrs_r_offset_max : FloatProperty(name = "Offset R max", description = "Offset for radius", default = .10000, min = 0)       
    change_z_co_flag : BoolProperty(name = "Change Z", description = "Change Z coordinate for after search", default = False)      
    change_z_co_val :  FloatProperty(name = "Change Z to", description = "Change Z coordinate value", default = 0)       

    # some quick functions
    def radius(self, x, y):
        return math.sqrt(x**2 + y**2)
    def min(self, a, b):
        return a if a is not None and b is not None and a < b else b  
    def max(self, a, b):
        return a if a is not None and b is not None and a > b else b    

    @classmethod
    def poll(cls, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        check_context = len([v for v in context.active_object.data.vertices if v.select]) > 0
        bpy.ops.object.mode_set(mode='EDIT')
        return check_context

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')  # can change selection only in Object mode
        # search for selected vertex and coordinates
        me = context.active_object.data
        z_min = z_max = r_min = r_max = None
        for vert in me.vertices:
            if vert.select:
                z_min = self.min(z_min, vert.co.z)
                z_max = self.max(z_max, vert.co.z)
                r_min = self.min(r_min, self.radius(vert.co.x, vert.co.y))
                r_max = self.max(r_max, self.radius(vert.co.x, vert.co.y))


        # claculating z threshholds with offsets
        threshold_z_min = z_min - self.thrs_z_offset_min
        threshold_z_max = z_max + self.thrs_z_offset_max
        

        # claculating radius and offsets
        threshold_r_min = r_min - self.thrs_r_offset_min if r_min > self.thrs_r_offset_min else 0
        threshold_r_max = r_max + self.thrs_r_offset_max


        # search and select vertices
        for vert in me.vertices:
            # select vertices that are between thresholds
            if (threshold_z_min <= vert.co.z <= threshold_z_max and threshold_r_min <= self.radius(vert.co.x, vert.co.y) <= threshold_r_max):
                vert.select = True
                # change z coordinate if needed
                if self.change_z_co_flag and self.change_z_co_val != None:
                    vert.co.z = self.change_z_co_val
                    
        bpy.ops.object.mode_set(mode='EDIT') 
        
                
        return {'FINISHED'}
    
    
# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SelectByRadiusOperator)


def unregister():
    bpy.utils.unregister_class(SelectByRadiusOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.select_by_radius()
