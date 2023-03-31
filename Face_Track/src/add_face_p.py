import bpy
from . import conf
from pathlib import Path
import numpy as np
import math
import os

def face_generator(img, cv2, mp):
    # empty image
    if img.shape == (1):
        conf.ShowMessageBox('Image is empty')
        return False 
    error, vertices = process_image(img, cv2, mp)
    if error is not None:
        conf.ShowMessageBox(error)
        return False

    faces = conf.MESH_FACES
    obj = create_obj(vertices, faces)
    crop_image_name = obj.name + "_cropped_face.jpg"

    if crop_image(img, crop_image_name, get_limits(vertices), get_addon_path(), cv2) != 0:
        return False
    transform(obj)
    unwrap_uv(obj)
    create_material(obj, obj.name + ".face_unwrapped", crop_image_name)
    obj[conf.FACE_PROPERTIE] = 1
    obj[conf.IS_PREPARED_PROPERTIE] = 0
    return True

def create_material(obj, mat_name, image_name):
    # Get material
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name=mat_name)
    else:
        if obj.data.materials:
            # assign to 1st material slot
            obj.data.materials[0] = mat
        else:
            # no slots
            obj.data.materials.append(mat)
            image = bpy.data.images.load(
                str(get_addon_path().joinpath(image_name))
                )
            mat.node_tree.nodes.get('Image Texture').image = image
            return
    # Assign it to object
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = mat
    else:
        # no slots
        obj.data.materials.append(mat)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled = mat.node_tree.nodes.get('Principled BSDF')
    image_n = nodes.new('ShaderNodeTexImage')
    image_n.location.xy = (principled.location.x - 2 *  principled.width, principled.location.y)
    mat.node_tree.links.new(principled.inputs[0], image_n.outputs[0])
    mat.node_tree.links.new(principled.inputs[7], image_n.outputs[0])
    image = bpy.data.images.load(
        str(get_addon_path().joinpath(image_name))
        )
    image_n.image = image


def unwrap_uv(obj):
    # create camera
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(9, 0, 0), rotation=(1.5708, 0, 1.5708),
                              scale=(1, 1, 1))
    my_cam = bpy.context.view_layer.objects.active
    bpy.context.scene.camera = my_cam
    # set view to camera
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_perspective = 'CAMERA'
            break
    # delete camera
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.editmode_toggle()
    # unwrap
    bpy.ops.mesh.select_all(action='SELECT')
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region, 'edit_object': bpy.context.edit_object}
                    bpy.ops.uv.project_from_view(override, camera_bounds=False, correct_aspect=True,
                                                 scale_to_bounds=True)
    bpy.ops.object.editmode_toggle()
    bpy.context.view_layer.objects.active = my_cam
    bpy.ops.object.delete(use_global=False)


def get_limits(res_arr):
    min_x = int(min(res_arr[0:, 0:1]) * 100)
    max_x = int(max(res_arr[0:, 0:1]) * 100)
    min_y = int(min(res_arr[0:, 1:2]) * 100)
    max_y = int(max(res_arr[0:, 1:2]) * 100)
    return (min_y, max_y, min_x, max_x)


def crop_image(image, crop_name, limits, path, cv2):
    try:
        crop_img = image[limits[0]:limits[1], limits[2]:limits[3]]
        cv2.imwrite(str(path.joinpath(crop_name)), crop_img)
    # failed to write image
    except:
        conf.ShowMessageBox("can not create image texture")
        return -1
    return 0


def get_addon_path():
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    path = Path(directory)
    return path


def capture_img(cv2):
    if cv2 == None:
        return np.zeros(1)
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image, 1)
        cv2.putText(image, text="Press Space to take a picture", org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(100, 255, 0), thickness=1)
        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(30) & 0xFF == ord(' '):
            cap.release()
            cv2.destroyAllWindows()
            return image


def process_image(image, cv2, mp):
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5) as face_mesh:
        # Convert the BGR image to RGB before processing.
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        res_arr = np.empty((478, 3))
        if not results.multi_face_landmarks:
            print('Landmarks was not created')
            return ("Face not found", [])
        else:
            print('lendmarks was created')
            for i, landmark in enumerate(results.multi_face_landmarks[0].landmark):
                res_arr[i] = conf.convert_units([landmark.x, landmark.y, landmark.z], image.shape)

            return (None, res_arr)


def create_obj(vertices, faces):
    # make mesh
    face_mesh = bpy.data.meshes.new('face_mesh')
    face_mesh.from_pydata(vertices, [], faces)
    face_mesh.update()

    # make object
    face_object = bpy.data.objects.new('face_mesh', face_mesh)

    # make collection
    if len(bpy.data.collections) == 0:
        face_track_collection = bpy.data.collections.new('face_track')
        bpy.context.scene.collection.children.link(face_track_collection)
    else:
        face_track_collection = bpy.data.collections[0]
        for col in bpy.data.collections:
            if col.name == 'face_track':
                face_track_collection = col
        if 'face_track' != face_track_collection.name:
            face_track_collection = bpy.data.collections.new('face_track')
            bpy.context.scene.collection.children.link(face_track_collection)

    # add object to scene collection
    face_track_collection.objects.link(face_object)

    return face_object


def transform(face_object):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects[face_object.name].select_set(True)

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.context.scene.objects[face_object.name].location = [0, 0, 0]
    face_object.rotation_euler.x -= math.radians(90)
    face_object.rotation_euler.z += math.radians(90)

    bpy.ops.object.shade_smooth()