import bpy, bmesh
from .src import conf
from .src.prepare_face_p import *




class Prepare_face(bpy.types.Operator):
    bl_idname = 'mesh.prepare_face'
    bl_label = 'Prepare Face'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = ("Create rig for the selected mesh")

    def execute(self, context):
        obj = context.active_object
        
        # Add empties to each vertex
        add_empty(obj)

        # Add armature and copy location modifier
        add_rig(obj)

        # Hide all the messy stuff(empty and rig)
        hide_rig(obj)

        # Set propertie
        obj[conf.IS_PREPARED_PROPERTIE] = 1
        return {"FINISHED"}
        

    @classmethod
    def poll(cls, context):
        return conf.check_operator(cls, context.active_object, 1, 0)

def register():
    bpy.utils.register_class(Prepare_face)


def unregister():
    bpy.utils.unregister_class(Prepare_face)




