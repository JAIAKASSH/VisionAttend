import cv2
import face_recognition
import os
import pickle
from datetime import datetime
from attendance_logger import log_attendance
from utils import load_encodings

ENCODINGS_DIR = "encodings"

def recognize_faces():
    known_encodings, known_names = load_encodings(ENCODINGS_DIR)
    attendance_today = set()  # Prevent double marking

    video_capture = cv2.VideoCapture(0)
    frame_count = 0

    print("[INFO] Starting real-time recognition...")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Failed to capture frame")
            break

        frame_count += 1
        if frame_count % 3 != 0:
            continue

        # Resize frame for speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = small_frame[:, :, ::-1]

        # Detect faces and encode
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding, location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.45)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]

                if name not in attendance_today:
                    log_attendance(name)
                    attendance_today.add(name)

            top, right, bottom, left = [v * 4 for v in location]  # Rescale to original size
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

        cv2.imshow("Face Recognition Attendance", frame)

        # Exit loop on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
