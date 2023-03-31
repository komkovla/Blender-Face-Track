from bpy.props import StringProperty
from .src.video_track_p import *
from bpy_extras.io_utils import ImportHelper





class Video_track_camera(bpy.types.Operator):
    bl_idname = 'mesh.video_track_camera'
    bl_label = 'from Camera'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = ("Record the animation of the face using web camera")

    def execute(self, context):
        trackers = get_trackers(context.active_object)
        if trackers == None:
            return {"FINISHED"}
        video_tracking(context.active_object)
        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        return conf.check_operator(cls, context.active_object, 1, 1)


class Video_track_video(bpy.types.Operator, ImportHelper):
    bl_idname = 'mesh.video_track_video'
    bl_label = 'from Video'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = ("Record the animation of the face using video from your computer")

    filter_glob: StringProperty(
        default='*.MOV;*.MP4;*.avi',
        options={'HIDDEN'}
    )
    def execute(self, context):
        trackers = get_trackers(context.active_object)
        if trackers == None:
            return {"FINISHED"}
        video_tracking(context.active_object, webcam_input= False, path = self.filepath)
        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        return conf.check_operator(cls, context.active_object, 1, 1)


def register():
    bpy.utils.register_class(Video_track_camera)
    bpy.utils.register_class(Video_track_video)


def unregister():
    bpy.utils.unregister_class(Video_track_camera)
    bpy.utils.unregister_class(Video_track_video)

