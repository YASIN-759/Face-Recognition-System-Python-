import tkinter as tk
import os

def show_instructions(parent=None):
    """
    Display the instructions.
    If a parent is provided, clear its content and display the instructions in that window.
    Otherwise, create a new Tk window.
    """
    if parent:
        # Clear all widgets from the parent window
        for widget in parent.winfo_children():
            widget.destroy()
        window = parent
    else:
        window = tk.Tk()

    window.title("Instructions")
    window.configure(bg="#0A192F")

    instructions = (
        "Instructions:\n\n"
        "1) Click on \"Student Details\" to add details\n"
        "2) Click on \"Student Details\" then click on \"View Record\" to see and note your record ID\n"
        "3) Click on \"Photo\" and enter your record ID to save your face information as a dataset, then click on \"Capture\" to save your dataset\n"
        "4) Click on \"Train Data\" and enter your ID then click on \"Start Training\" to train the algorithm on your dataset\n"
        "5) Click on \"Face Recognition\" for face detection; it will mark your attendance as well\n"
        "6) Click on \"Attendance\" to ensure and see the marked attendance\n"
    )

    label = tk.Label(window, text=instructions, justify="left",
                     font=("Arial", 14), bg="#0A192F", fg="white")
    label.pack(padx=20, pady=20)
    
    def go_to_main():
        # Destroy the current window and then open main_ui.py
        window.destroy()
        os.system("python main_ui.py")
    
    back_button = tk.Button(window, text="Go to Main", font=("Arial", 14, "bold"),
                            bg="red", fg="white", command=go_to_main)
    back_button.pack(pady=10)

    # If no parent was provided, start the main loop.
    if not parent:
        window.mainloop()

if __name__ == "__main__":
    show_instructions()
