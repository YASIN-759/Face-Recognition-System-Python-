

from tkinter import *
from PIL import Image, ImageTk
import main_ui
import pymysql

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)  # Start in fullscreen
        self.root.configure(bg="#0A192F")
        self.root.title("Login - Face Recognition System")

        # Bind Escape to exit fullscreen and resize
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Background Image
        bg_img = Image.open(r"C:\Users\admin\Downloads\face_recognition system (1)\face_recognition system\Designing Images\form1.webp")
        bg_img = bg_img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Login Frame
        login_frame = Frame(self.root, bg="#0A192F", bd=5, relief=RIDGE)
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=450)

        Label(login_frame, text="LOGIN", font=("Arial", 24, "bold"), fg="#00FFFF", bg="#0A192F").pack(pady=20)
        Label(login_frame, text="Username:", font=("Arial", 16), fg="#FFFFFF", bg="#0A192F").pack()

        self.username_entry = Entry(login_frame, font=("Arial", 14), width=30)
        self.username_entry.pack(pady=5)

        Label(login_frame, text="Password:", font=("Arial", 16), fg="#FFFFFF", bg="#0A192F").pack()
        self.password_entry = Entry(login_frame, font=("Arial", 14), show="*", width=30)
        self.password_entry.pack(pady=5)

        self.error_label = Label(login_frame, text="", font=("Arial", 12), fg="red", bg="#0A192F")
        self.error_label.pack()

        Button(login_frame, text="Login", font=("Arial", 14, "bold"), bg="#00FFFF", fg="#000000", command=self.authenticate).pack(pady=15)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        self.root.geometry("1350x800")

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.username_entry.config(highlightthickness=0, highlightbackground="#0A192F")
        self.password_entry.config(highlightthickness=0, highlightbackground="#0A192F")
        self.error_label.config(text="")

        if not username or not password:
            self.error_label.config(text="Please fill in all fields!")
            if not username:
                self.username_entry.config(highlightthickness=2, highlightbackground="red")
            if not password:
                self.password_entry.config(highlightthickness=2, highlightbackground="red")
            return

        try:
            conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin_credentials WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                self.root.destroy()
                root_main = Tk()
                main_ui.FaceRecognitionApp(root_main)
                root_main.mainloop()
            else:
                self.error_label.config(text="Wrong credentials!")
                self.username_entry.config(highlightthickness=2, highlightbackground="red")
                self.password_entry.config(highlightthickness=2, highlightbackground="red")

        except Exception as e:
            self.error_label.config(text=f"Error connecting to DB: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = LoginApp(root)
    root.mainloop()
