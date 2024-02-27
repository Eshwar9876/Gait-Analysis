import os
import cv2
import pickle
import mediapipe as mp
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def make_segmenation_file(filename, classname, show_points = False):
    video_points = []
    classes = []
    print(f'[info] Converting {filename} ...')
    cap = cv2.VideoCapture(filename)
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            current_frame_points = []
            for current_points in results.pose_landmarks.landmark:
                current_frame_points.append([current_points.x, current_points.y, current_points.z])

            video_points.append([np.array(current_frame_points), classname])
            if classname not in classes:
                classes.append(classname)

            if show_points:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()

    DATABASE_PATH = os.path.join(os.getcwd(), 'dataset', 'data.pkl')
    CLASSES_PATH = os.path.join(os.getcwd(), 'dataset', 'classes.pkl')
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'rb') as fl:
            data = pickle.load(fl)
            data.extend(video_points)
        pickle.dump(data, open(DATABASE_PATH, 'wb')) 

        with open(CLASSES_PATH, 'rb') as fl:
            data = pickle.load(fl)
            data.extend(classes)
        pickle.dump(data, open(CLASSES_PATH, 'wb')) 

    else:
        pickle.dump(video_points, open(DATABASE_PATH, 'wb')) 
        pickle.dump(classes, open(CLASSES_PATH, 'wb'))


def make_segmenation(show_points = False):
    VIDEO_PATH = os.path.join(os.getcwd(), 'videos')
    video_points = []
    classes = []
    for current_video in os.listdir(VIDEO_PATH):
        print(f'[info] Converting {current_video} ...')
        cap = cv2.VideoCapture(os.path.join(VIDEO_PATH, current_video))
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    break

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                current_frame_points = []
                for current_points in results.pose_landmarks.landmark:
                    current_frame_points.append([current_points.x, current_points.y, current_points.z])

                video_points.append([np.array(current_frame_points), os.path.splitext(current_video)[0]])
                if os.path.splitext(current_video)[0] not in classes:
                    classes.append(os.path.splitext(current_video)[0])

                if show_points:
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

            cap.release()

    DATABASE_PATH = os.path.join(os.getcwd(), 'dataset', 'data.pkl')
    CLASSES_PATH = os.path.join(os.getcwd(), 'dataset', 'classes.pkl')
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'rb') as fl:
            data = pickle.load(fl)
            data.extend(video_points)
        pickle.dump(data, open(DATABASE_PATH, 'wb')) 

        with open(CLASSES_PATH, 'rb') as fl:
            data = pickle.load(fl)
            data.extend(classes)
        pickle.dump(classes, open(CLASSES_PATH, 'wb')) 

    else:
        pickle.dump(video_points, open(DATABASE_PATH, 'wb')) 
        pickle.dump(classes, open(CLASSES_PATH, 'wb'))


if __name__ == '__main__':
    make_segmenation()