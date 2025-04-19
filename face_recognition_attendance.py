
import cv2
import numpy as np
import pymysql
import os
from datetime import datetime

def mark_attendance(roll_no):
    conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            roll INT PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(100),
            status VARCHAR(10) DEFAULT 'absent'
        )
    """)
    conn.commit()

    cursor.execute("SELECT name, department FROM students WHERE roll = %s", (roll_no,))
    student_info = cursor.fetchone()
    if student_info is None:
        print(f"No student details found for Roll No {roll_no}")
        conn.close()
        return

    name, department = student_info

    cursor.execute("SELECT * FROM attendance WHERE roll = %s", (roll_no,))
    existing = cursor.fetchone()
    if existing is None:
        cursor.execute("""
            INSERT INTO attendance (roll, name, department, status)
            VALUES (%s, %s, %s, 'present')
        """, (roll_no, name, department))
    else:
        cursor.execute("UPDATE attendance SET status = 'present' WHERE roll = %s", (roll_no,))

    conn.commit()
    print(f"Attendance marked as present for Roll No {roll_no} - {name}")
    conn.close()

def load_training_data():
    conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
    cursor = conn.cursor()
    cursor.execute("SELECT roll, pictures FROM students WHERE pictures IS NOT NULL AND pictures != ''")
    records = cursor.fetchall()
    conn.close()

    face_samples = []
    labels = []
    cascade_path = "haarcascade_frontalface_default.xml"
    face_detector = cv2.CascadeClassifier(cascade_path)
    if face_detector.empty():
        print("Error: Could not load Haar Cascade from", cascade_path)
        return [], []

    for roll, folder in records:
        folder = folder.decode() if isinstance(folder, bytes) else folder
        if os.path.exists(folder):
            image_files = [f for f in os.listdir(folder)
                           if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
            for image_file in image_files:
                img_path = os.path.join(folder, image_file)
                img = cv2.imread(img_path)
                if img is None:
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                for (x, y, w, h) in faces:
                    face_samples.append(gray[y:y+h, x:x+w])
                    labels.append(int(roll))
                    break
    return face_samples, labels

def main():
    cascade_path = "haarcascade_frontalface_default.xml"
    faces, labels = load_training_data()
    if len(faces) == 0:
        print("No training data available! Ensure that training images exist for at least one student.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Starting the face recognition attendance system...")
    face_detector = cv2.CascadeClassifier(cascade_path)
    if face_detector.empty():
        print("Error: Could not load Haar Cascade from", cascade_path)
        return

    THRESHOLD = 80

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_detected = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces_detected:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.equalizeHist(face_roi)
            roll_no, confidence = recognizer.predict(face_roi)

            if confidence < THRESHOLD:
                label = f"Roll: {roll_no} ({round(confidence, 2)})"
                color = (0, 255, 0)
                mark_attendance(roll_no)
            else:
                label = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("Face Recognition Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()