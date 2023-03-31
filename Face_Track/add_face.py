from bpy.props import StringProperty
from bpy.props import CollectionProperty
from .src.add_face_p import *
from pathlib import Path

from .src import conf
from bpy_extras.io_utils import ImportHelper

class addFace_camera(bpy.types.Operator):
    bl_idname = 'mesh.add_face_camera'
    bl_label = 'From Camera'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = ("Creates face mesh from your webcam input")

    def execute(self, context):
        # Check modules
        if self.cv2 == None or self.mp == None:
            return {"CANCELLED"}
        
        # Capture image
        try:
            img = capture_img(self.cv2)
        except:
            conf.ShowMessageBox("Can not capture image, there might be problem with you web cam")
            return {"CANCELLED"}
        
        # Generate mesh
        try:
            face_generator(img, self.cv2, self.mp)
        except:
            conf.ShowMessageBox("Can not generate mesh from the image there might be problem with mediapipe")
            return {"CANCELLED"}

        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        return conf.MODULES_INSTALLED

    def invoke(self, context, _):
        self.cv2 = conf.import_module('cv2')
        self.mp = conf.import_module('mediapipe')
        return self.execute(context)

class addFace_photo(bpy.types.Operator, ImportHelper):
    bl_idname = 'mesh.add_face_photo'
    bl_label = 'From photo'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = ("Creates face mesh from image on your computer")

    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp',
        options={'HIDDEN'}
    )

    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )

    def execute(self, context):
        # Check modules

        self.cv2 = conf.import_module('cv2')
        self.mp = conf.import_module('mediapipe')
        if self.cv2 == None or self.mp == None:
            return {"CANCELLED"}
        
        for file in self.files:
            folder_path = Path(self.filepath).parent
            print(folder_path)
            file_path = str(folder_path.joinpath(file.name))
            print(file_path)
            # Get image
            try:
                img = self.cv2.imread(file_path)
            except:
                conf.ShowMessageBox("Can't read the image")
                return {"CANCELLED"}
            # Generate mesh
            face_generator(img, self.cv2, self.mp)

        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        cls.poll_message_set("Modules are not installed")
        return conf.MODULES_INSTALLED


def register():
    bpy.utils.register_class(addFace_camera)
    bpy.utils.register_class(addFace_photo)


def unregister():
    bpy.utils.unregister_class(addFace_camera)
    bpy.utils.unregister_class(addFace_photo)


