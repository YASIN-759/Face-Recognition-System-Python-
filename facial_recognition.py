

import cv2
import os
import pymysql
import numpy as np
from tkinter import *
from tkinter import messagebox

class FacialRecognitionTrainer:
    def __init__(self, root):
        self.top = Toplevel(root)
        self.top.title("Train Facial Recognition Data")
        self.top.attributes("-fullscreen", True)  # Start in fullscreen
        self.top.configure(bg="#0A192F")

        # Bind Escape key to exit fullscreen and set fixed size
        self.top.bind("<Escape>", self.exit_fullscreen)

        Label(self.top, text="Enter Roll No:", font=("Arial", 14), bg="#0A192F", fg="white").pack(pady=20)
        self.entry_roll = Entry(self.top, font=("Arial", 14), width=30)
        self.entry_roll.pack(pady=10)

        Button(self.top, text="Start Training", font=("Arial", 14, "bold"), bg="#00FFFF", fg="black",
               command=self.start_training).pack(pady=20)

        self.status_label = Label(self.top, text="", font=("Arial", 12), bg="#0A192F", fg="white")
        self.status_label.pack(pady=10)

        self.progress = Label(self.top, text="", font=("Arial", 10), bg="#0A192F", fg="yellow")
        self.progress.pack(pady=5)

        Button(self.top, text="Back", font=("Arial", 12), bg="#FF6666", fg="white",
               command=self.go_back).pack(pady=10)

    def exit_fullscreen(self, event=None):
        self.top.attributes("-fullscreen", False)
        self.top.geometry("1350x800")

    def go_back(self):
        self.top.destroy()  # Close current window
        os.system("python main_ui.py")  # Open main UI (adjust path if needed)

    def start_training(self):
        roll_no = self.entry_roll.get().strip()
        if not roll_no:
            messagebox.showerror("Error", "Please enter a roll number!")
            return

        try:
            roll_no_int = int(roll_no)
        except ValueError:
            messagebox.showerror("Error", "Roll number must be an integer!")
            return

        try:
            conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
            cursor = conn.cursor()

            cursor.execute("SELECT pictures, train_data FROM students WHERE roll = %s", (roll_no_int,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "No student found with this Roll No!")
                conn.close()
                return

            dataset_path, trained_status = result
            if not dataset_path or not os.path.exists(dataset_path):
                messagebox.showerror("Error", "Pictures dataset not found or path is invalid!")
                conn.close()
                return

            if trained_status == "yes":
                messagebox.showinfo("Info", "This student's dataset is already trained!")
                conn.close()
                return

        except Exception as e:
            messagebox.showerror("DB Error", f"Failed to fetch student data:\n{e}")
            return

        self.status_label.config(text="Starting training...")
        self.top.update()

        cascade_path = "haarcascade_frontalface_default.xml"
        if not os.path.exists(cascade_path):
            messagebox.showerror("Error", "Haar Cascade file not found!")
            return

        face_detector = cv2.CascadeClassifier(cascade_path)
        if face_detector.empty():
            messagebox.showerror("Error", "Failed to load Haar Cascade!")
            return

        faces = []
        ids = []

        image_files = [f for f in os.listdir(dataset_path) if f.lower().endswith((".jpg", ".png", ".jpeg", ".webp"))]
        if len(image_files) == 0:
            messagebox.showerror("Error", "No image files found in dataset!")
            return

        total_files = len(image_files)
        count = 0

        for image_file in image_files:
            image_path = os.path.join(dataset_path, image_file)
            img = cv2.imread(image_path)
            if img is None:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            detected_faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in detected_faces:
                faces.append(gray[y:y+h, x:x+w])
                ids.append(roll_no_int)

            count += 1
            self.progress.config(text=f"Processed {count}/{total_files} images")
            self.top.update()

        if len(faces) == 0:
            messagebox.showerror("Error", "No faces detected in dataset!")
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
        except AttributeError:
            messagebox.showerror("Error", "LBPH Face Recognizer not available. Install opencv-contrib-python.")
            return

        recognizer.train(faces, np.array(ids))
        recognizer.save("trained_model.yml")

        try:
            cursor.execute("ALTER TABLE students ADD COLUMN train_data VARCHAR(10) DEFAULT 'no'")
            conn.commit()
        except:
            pass  # Column may already exist

        try:
            cursor.execute("UPDATE students SET train_data = 'yes' WHERE roll = %s", (roll_no_int,))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not update training status:\n{e}")
            return

        self.status_label.config(text="Training completed successfully!")
        self.progress.config(text="")
        messagebox.showinfo("Success", "Facial recognition model trained and saved as trained_model.yml")

# Example usage:
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the main root window
    FacialRecognitionTrainer(root)
    root.mainloop()
