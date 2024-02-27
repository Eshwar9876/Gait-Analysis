import cv2
import numpy as np



def detect_pose(frame, mp_drawing, mp_drawing_styles, mp_pose, pose, model, classes_list, show_points=False):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)

    current_frame_points = []

    try:
        aa = results.pose_landmarks.landmark
    except:
        return frame, []

    for current_points in results.pose_landmarks.landmark:
        current_frame_points.append([current_points.x, current_points.y, current_points.z])

    if show_points:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
    current_frame_points = np.array(current_frame_points).reshape(-1, 33, 3)
    result = np.argmax(model.predict(current_frame_points), axis=1)
    cv2.putText(frame, f"Person: {classes_list[result[0]]}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    return frame, current_frame_points 