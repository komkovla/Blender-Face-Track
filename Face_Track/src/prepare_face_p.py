import bpy, bmesh
from . import conf


def hide_rig(obj):
    bpy.data.collections[obj.name + conf.TRACKER_COL_NAME].hide_viewport = True
    bpy.data.objects[obj.name + ".armature"].hide_set(True)



def add_empty(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.transform_apply()

    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(obj.data)
        verts = [vert.co for vert in bm.verts]
    else:
        verts = [vert.co for vert in obj.data.vertices]

    # coordinates as tuples
    plain_verts = [vert.to_tuple() for vert in verts]
    col = get_col(obj.name + conf.TRACKER_COL_NAME)
    for index, coord in enumerate(plain_verts):
        
        obj_empty = bpy.data.objects.new(obj.name + ".tracker." + str(index), None)
        col.objects.link(obj_empty)
        obj_empty.location = coord
        obj_empty.scale = (0.15, 0.15, 0.15)

def get_col(collection_name):
    for col in bpy.data.collections:
        if col.name == collection_name:
            return col
    print("new_col")
    face_track_collection = bpy.data.collections.new(collection_name)
    bpy.data.collections[conf.FACE_COL_NAME].children.link(face_track_collection)
    return face_track_collection


def add_rig(obj):
    # face mesh setup
    trackers = bpy.data.collections[obj.name + conf.TRACKER_COL_NAME].objects
    bones = []
    for tracker in trackers:
        bpy.ops.object.armature_add(enter_editmode=False, location=tracker.location)
        bone = bpy.context.object
        bones.append(bone)
    for bone in bones:
        bone.select_set(True)
    # join armatures in correct order
    bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
    bpy.ops.object.join()
    arm = bpy.data.objects['Armature']
    arm.name = obj.name + ".armature"
    bpy.ops.object.transform_apply()

    # parent face to bones
    obj.select_set(True)
    arm.select_set(True)
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    bpy.ops.object.posemode_toggle()
    for i, bone in enumerate(arm.data.bones):
        arm.data.bones.active = bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones[bone.name].constraints["Copy Location"].target = trackers[i]
        bone.select = False
    bpy.ops.object.posemode_toggle()