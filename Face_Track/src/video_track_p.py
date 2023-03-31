import bpy
from . import conf
import numpy as np
import time

def get_trackers(obj):
    try:
        return bpy.data.collections[obj.name + conf.TRACKER_COL_NAME].objects
    except KeyError:
        conf.ShowMessageBox('Can not find trackers collection')
        return None

def video_tracking(obj, webcam_input = True, path = ''):
    cv2 = conf.import_module('cv2')
    mp = conf.import_module('mediapipe')
    mp_face_mesh = mp.solutions.face_mesh

    def retime_key_frames(face_obj, trackers, multiplication):
        bpy.ops.object.select_all(action='DESELECT')
        # Need to show for keyframes to apperar in graph_editor
        bpy.data.collections[face_obj.name + conf.TRACKER_COL_NAME].hide_viewport = False
        # Select all the trackers
        for obj in trackers:
            obj.select_set(True)

        # Change area type
        old_type = bpy.context.area.type
        bpy.context.area.type = 'GRAPH_EDITOR'
        # change interpolation type
        # bpy.ops.graph.interpolation_type(type='CONSTANT')
        # Set pivot to the start
        bpy.context.scene.frame_current = 1
        bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.ops.transform.resize(value=(multiplication, 1, 1))
        # Return area type
        bpy.context.area.type = old_type
        # Hide trackers
        bpy.data.collections[face_obj.name + conf.TRACKER_COL_NAME].hide_viewport = True

    def process_image(image, tracker_loc):
        with mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5) as face_mesh:
            # Convert the BGR image to RGB before processing.
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if not results.multi_face_landmarks:
                print('Landmarks was not created')
            else:
                for i, landmark in enumerate(results.multi_face_landmarks[0].landmark):
                    tracker_loc[i] = conf.convert_units([landmark.x, landmark.y, landmark.z], image.shape)

    # For webcam input:
    if webcam_input:
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(path)
    first = True
    frame = 1
    scale_key_frame = 0
    trackers = bpy.data.collections[obj.name + conf.TRACKER_COL_NAME].objects
    for tracker in trackers:
        tracker.animation_data_clear()
    tracker_loc = np.empty((478, 3))
    tracker_loc_old = np.empty((478, 3))
    prev_frame_time = 0
    new_frame_time = 0
    fps_sum = 0
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            time.sleep(0.1)
            # Read image
            success, image = cap.read()
            if not success:
                if webcam_input:
                    print("Ignoring empty camera frame.")
                    continue
                else:
                    scale_key_frame = 24 / (fps_sum / frame)
                    break
            image.flags.writeable = False
            
            # Process image
            process_image(image, tracker_loc)
            tracker_loc_tmp = tracker_loc

            bpy.context.scene.frame_set(frame)
            # Recording difference between last 2 positions
            if not first:
                tracker_loc = tracker_loc - tracker_loc_old
                for i, tracker in enumerate(trackers):
                    # xyz- tracking
                    tracker_loc[i] = [-tracker_loc[i][2], tracker_loc[i][0], -tracker_loc[i][1]]
                    # xy -tracking
                    # tracker_loc[i] = [-tracker_loc[i][2],tracker_loc[i][0],0]

                    tracker_loc[i] += tracker.matrix_world.translation
                    tracker.location = tracker_loc[i].tolist()

                    tracker.keyframe_insert(data_path="location")
            first = False
            # setting new position as the old one
            tracker_loc_old = tracker_loc_tmp

            # fps_counter
            image.flags.writeable = True
            new_frame_time = time.time()
            # Calculating the fps
            fps = 1 / (new_frame_time - prev_frame_time)
            fps_sum += fps
            prev_frame_time = new_frame_time
            # putting the FPS count on the frame
            image = cv2.flip(image, 1)
            if conf.DEBUG:
                cv2.putText(image, text="FPS: %s" % str(int(fps)), org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(100, 255, 0), thickness=1)
            else:
                cv2.putText(image, text="Press space to exit", org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(100, 255, 0), thickness=1)
            cv2.imshow('MediaPipe Face Mesh', image)
            
            # Stop video stream on 'Space' press
            if cv2.waitKey(33) & 0xFF == ord(' '):
                scale_key_frame = 24 / (fps_sum / frame)
                cap.release()
                cv2.destroyAllWindows()
                break
            frame += 1
    # update view layer
    bpy.context.view_layer.update()
    retime_key_frames(obj, trackers, scale_key_frame)