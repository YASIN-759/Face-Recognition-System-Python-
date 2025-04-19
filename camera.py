

import cv2
import pymysql
import os
from tkinter import messagebox, Label, Button, Entry, Tk

class CameraUse:
    def __init__(self, root):
        """Initialize the camera window within the same main window."""
        self.root = root
        self.root.title("Capture Images")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.configure(bg="#0A192F")  # Apply background color

        # Remove all previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Label and Entry for Roll No
        Label(self.root, text="Enter Roll No:", font=("Arial", 12), bg="#0A192F", fg="white").pack(pady=10)
        self.entry_roll = Entry(self.root, font=("Arial", 12))
        self.entry_roll.pack(pady=10)
        
        # Capture Button
        Button(self.root, text="Capture", font=("Arial", 12, "bold"), bg="green", fg="white", 
               command=self.capture_images).pack(pady=10)
        
        # Back to Main Button
        Button(self.root, text="Back to Main", font=("Arial", 14, "bold"), bg="red", fg="white",
               command=self.load_main_ui).pack(pady=10)

    def exit_fullscreen(self):
        self.root.attributes('-fullscreen', False)
        self.root.geometry("1351x800") 

    def capture_images(self):
        """Capture 50 images, convert them to grayscale, and store the directory path in the database."""
        
        roll_no = self.entry_roll.get().strip()
        if not roll_no:
            messagebox.showerror("Error", "Roll No cannot be empty!")
            return

        try:
            roll_int = int(roll_no)  # Ensure the Roll No is an integer
        except ValueError:
            messagebox.showerror("Error", "Roll No must be a valid number.")
            return
        
        # Connect to MySQL database
        conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
        cursor = conn.cursor()
        
        # Check if the Roll No exists in the database
        cursor.execute("SELECT roll FROM students WHERE roll = %s", (roll_int,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", f"Roll No {roll_int} not found in database!")
            conn.close()
            return

        # Create directory to save images
        img_dir = os.path.join("dataset", str(roll_int))
        os.makedirs(img_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(0)  # Open webcam

        for i in range(50):
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break
            
            # Convert the captured frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Debug: print shapes of the original and grayscale images
            print(f"Image {i+1}: Original shape {frame.shape}, Grayscale shape {gray_frame.shape}")
            
            img_path = os.path.join(img_dir, f"img_{i+1}.jpg")
            cv2.imwrite(img_path, gray_frame)  # Save the grayscale image
            
            cv2.imshow("Capturing Images", gray_frame)
            cv2.waitKey(100)  # Wait 100ms before taking the next image
        
        cap.release()
        cv2.destroyAllWindows()

        # Store the folder path in the database for the given Roll No
        img_dir = os.path.abspath(img_dir)  # Convert to absolute path to avoid issues with relative paths
        cursor.execute("UPDATE students SET pictures = %s WHERE roll = %s", 
                       (img_dir, roll_int))
        conn.commit()
        
        messagebox.showinfo("Success", f"50 grayscale images captured and stored in {img_dir}!")
        conn.close()

    def load_main_ui(self):
        """Close current window and open main_ui.py."""
        self.root.destroy()
        os.system("python main_ui.py")  # Make sure main_ui.py is in the same directory

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = CameraUse(root)
    root.mainloop()
