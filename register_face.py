import cv2
import face_recognition
import os
import pickle
from controller_login import verify_login

ENCODINGS_DIR = "encodings"
FACES_DIR = "faces"
os.makedirs(ENCODINGS_DIR, exist_ok=True)
os.makedirs(FACES_DIR, exist_ok=True)

def register_new_face():
    if not verify_login():
        return

    name = input("Enter name of new user: ").strip()
    person_dir = os.path.join(FACES_DIR, name)
    os.makedirs(person_dir, exist_ok=True)

    video_capture = cv2.VideoCapture(0)
    images = []
    print("[INFO] Capturing face images. Press 'q' to finish.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            continue

        cv2.imshow("Registering", frame)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break

        images.append(frame)

    video_capture.release()
    cv2.destroyAllWindows()

    encodings = []
    for img in images:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb_img)
        if boxes:
            encoding = face_recognition.face_encodings(rgb_img, boxes)[0]
            encodings.append(encoding)

    if encodings:
        avg_encoding = sum(encodings) / len(encodings)
        with open(os.path.join(ENCODINGS_DIR, f"{name}.pkl"), "wb") as f:
            pickle.dump({"name": name, "encoding": avg_encoding}, f)
        print(f"[SAVED] Encoding for {name} saved.")
    else:
        print("[ERROR] No face detected.")