
from tkinter import *
from PIL import Image, ImageTk
import student_detail 
import camera
import facial_recognition
import face_recognition_attendance  
import attendance_view  
import help

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.configure(bg="#0A192F")
        self.root.title("Face Recognition System")

        Label(self.root, text="FACE RECOGNITION SYSTEM", font=("Arial", 24, "bold"), fg="#00FFFF", bg="#0A192F").pack(pady=20)

        img_main = Image.open(r"C:\Users\admin\Downloads\face_recognition system (1)\face_recognition system\Designing Images\1.webp")
        img_main = img_main.resize((1000, 1000), Image.Resampling.LANCZOS)
        self.photoimg_main = ImageTk.PhotoImage(img_main)
        Label(self.root, image=self.photoimg_main, bg="#0A192F").place(relx=0.508, rely=0.425, anchor=CENTER)

        self.scan_line = Label(self.root, bg="#00FFFF", height=2, width=80)
        self.scan_line.place(x=460, y=150)
        self.animate_scan()

    def exit_fullscreen(self):
        self.root.attributes('-fullscreen', False)
        self.root.geometry("1351x800")  # Or any size you prefer

    def animate_scan(self):
        new_y = self.scan_line.winfo_y() + 15
        if new_y > 530:
            self.scan_line.place(y=530)
            self.root.after(1000, self.finalize_scan)
        else:
            self.scan_line.place(y=new_y)
            self.root.after(20, self.animate_scan)

    def finalize_scan(self):
        self.scan_line.place_forget()
        self.show_buttons()

    def open_sd(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        student_detail.StudentDetails(self.root)

    def open_cam(self):
        camera.CameraUse(self.root)
        
    def open_dt(self):
        # Open the facial recognition training window
        facial_recognition.FacialRecognitionTrainer(self.root)

    def open_attendance(self, event=None):
        # Open the attendance system (webcam based recognition)
        face_recognition_attendance.main()


    def open_attend_record(self):
        # import attendance_view
        attendance_view.main(self.root)
        
    def open_instruct(self):
        help.show_instructions(self.root)


    def show_buttons(self):
        left_buttons_x = 50
        right_buttons_x = self.root.winfo_width() - 250
        top_padding = 70
        button_y_positions = [100 + top_padding, 300 + top_padding, 500 + top_padding]

        positions = [
            (left_buttons_x, button_y_positions[0]),
            (left_buttons_x, button_y_positions[1]),
            (left_buttons_x, button_y_positions[2]),
            (right_buttons_x, button_y_positions[0]),
            (right_buttons_x, button_y_positions[1]),
            (right_buttons_x, button_y_positions[2])
        ]

        labels = ["Student Details", "Face Recognition", "Attendance", "Help", "Train Data", "Photos"]
        image_paths = [
            r"C:\Users\admin\Downloads\face_recognition system (1)\face_recognition system\Designing Images\StudentDetails.webp",
            r"C:\Users\admin\Downloads\face_recognition system (1)\face_recognition system\Designing Images\FaceRecognition.webp",
            r"C:\Users\admin\Downloads\face_recognition system (1)\face_recognition system\Designing Images\Attendance.webp",
            r"C:\Users\admin\Downloads\face_recognition system (1)\face_recognition system\Designing Images\Help.webp",
            r"C:\Users\admin\Downloads\face_recognition system (1)\face_recognition system\Designing Images\TrainData.webp",
            r"C:\Users\admin\Downloads\face_recognition system (1)\face_recognition system\Designing Images\Photos.webp"
        ]

        self.button_images = []
        for (x, y), text, img_path in zip(positions, labels, image_paths):
            img = Image.open(img_path)
            img = img.resize((130, 130), Image.Resampling.LANCZOS)
            photo_img = ImageTk.PhotoImage(img)
            self.button_images.append(photo_img)

            Label(self.root, image=photo_img, bg="#0A192F").place(x=x+35, y=y-130)
            # Map button text to corresponding command:
            if text == "Student Details":
                btn_command = self.open_sd
            elif text == "Face Recognition":
                btn_command = self.open_attendance
            elif text == "Train Data":
                btn_command = self.open_dt
            elif text == "Photos":
                btn_command = self.open_cam
            elif text == "Attendance":
                btn_command = self.open_attend_record
            elif text == "Help":
                btn_command = self.open_instruct
            else:
                btn_command = None

            btn = Button(self.root, text=text, font=("Arial", 14, "bold"), bg="#00FFFF", fg="#000000", 
                         width=18, height=1, cursor="hand2", command=btn_command)
            btn.place(x=x, y=y)

        Button(self.root, text="Exit", font=("Arial", 14, "bold"), bg="red", fg="white", command=self.root.quit, cursor="hand2").place(
            x=self.root.winfo_width()//2 - 50, y=600 + top_padding, width=100, height=40)

if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
