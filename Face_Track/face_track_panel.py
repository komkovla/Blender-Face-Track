import bpy
from . import add_face
from . import install_dep as dep
from . import prepare_face
from .src import conf
from . import video_track

class faceTrackPanel(bpy.types.Panel):
    bl_idname = "PREFERENCES_PT_face_track_panel"
    bl_label = "face track"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "face track"

    def draw(self, context):
        if not conf.MODULES_INSTALLED:
            self.layout.label(text="Please install dependancies from settings", icon = "INFO")
        
        # Generate face box
        box = self.layout.box()
        box.label(text="Generate Face", icon = "CUBE")
        row = box.row()
        row.operator(add_face.addFace_camera.bl_idname, icon='SCENE', text=add_face.addFace_camera.bl_label)
        row.operator(add_face.addFace_photo.bl_idname, icon='IMAGE_DATA', text=add_face.addFace_photo.bl_label)
        
        # Prepare face
        self.layout.label(text="Preparation could take up to a minute", icon = "INFO")
        self.layout.operator(prepare_face.Prepare_face.bl_idname, icon='MODIFIER', text=prepare_face.Prepare_face.bl_label)
        
        # Video capture
        box2 = self.layout.box()
        box2.label(text="Animate", icon = "MOD_ARMATURE")
        row2 = box2.row()
        row2.operator(video_track.Video_track_camera.bl_idname, icon='SCENE', text=video_track.Video_track_camera.bl_label)
        row2.operator(video_track.Video_track_video.bl_idname, icon='SEQUENCE', text=video_track.Video_track_video.bl_label)

def register():
    bpy.utils.register_class(faceTrackPanel)

def unregister():
    bpy.utils.unregister_class(faceTrackPanel)

