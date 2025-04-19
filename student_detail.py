

# from tkinter import *
# from tkinter import messagebox, ttk
# import pymysql
# import os

# class StudentDetails:
#     def __init__(self, root):
#         self.root = root
#         self.root.attributes('-fullscreen', True)
#         self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
#         self.root.title("Student Details")
#         self.root.configure(bg="#0A192F")

#         # Variables
#         self.var_name = StringVar()
#         self.var_dept = StringVar()
#         self.var_roll = StringVar()
#         self.var_email = StringVar()
#         self.var_phone = StringVar()
#         self.var_address = StringVar()
#         self.var_gender = StringVar()
#         self.var_dob = StringVar()
#         self.var_search = StringVar()

#         # Title
#         title_lbl = Label(self.root, text="STUDENT DETAILS", font=("Arial", 24, "bold"), bg="#0A192F", fg="#00FFFF")
#         title_lbl.pack(pady=20)

#         # Input Frame
#         input_frame = Frame(self.root, bg="#112240", bd=2, relief=RIDGE)
#         input_frame.place(x=30, y=100, width=600, height=600)

#         labels = [
#             ("Name", self.var_name),
#             ("Department", self.var_dept),
#             ("Roll No", self.var_roll),
#             ("Email", self.var_email),
#             ("Phone", self.var_phone),
#             ("Address", self.var_address),
#             ("Gender", self.var_gender),
#             ("DOB (YYYY-MM-DD)", self.var_dob),
#         ]

#         for i, (text, var) in enumerate(labels):
#             Label(input_frame, text=text, font=("Arial", 12, "bold"), bg="#112240", fg="white").grid(row=i, column=0, padx=10, pady=10, sticky=W)
#             Entry(input_frame, textvariable=var, font=("Arial", 12), width=25).grid(row=i, column=1, padx=10, pady=10)

#         # Button Frame
#         btn_frame = Frame(input_frame, bg="#112240")
#         btn_frame.place(x=10, y=480, width=570, height=60)

#         Button(btn_frame, text="Save", command=self.add_data, width=12, font=("Arial", 12, "bold"), bg="#00FFFF", fg="black").grid(row=0, column=0, padx=5)
#         Button(btn_frame, text="Reset", command=self.reset_fields, width=12, font=("Arial", 12, "bold"), bg="orange", fg="black").grid(row=0, column=1, padx=5)
#         Button(btn_frame, text="Cancel Edit", command=self.cancel_edit, width=12, font=("Arial", 12, "bold"), bg="#FFC107", fg="black").grid(row=0, column=2, padx=5)
#         Button(btn_frame, text="Delete", command=self.delete_record, width=12, font=("Arial", 12, "bold"), bg="#FF4C4C", fg="white").grid(row=0, column=3, padx=5)
#         Button(btn_frame, text="Back", command=self.go_to_main, width=12, font=("Arial", 12, "bold"), bg="red", fg="white").grid(row=1, column=0, columnspan=4, pady=5)

#         # Table Frame for records
#         record_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#112240")
#         record_frame.place(x=650, y=100, width=690, height=600)

#         Entry(record_frame, textvariable=self.var_search, font=("Arial", 12)).pack(pady=5)
#         Button(record_frame, text="Search", command=self.search_record, bg="#00FFFF", font=("Arial", 12)).pack(pady=5)

#         # Scrollbars
#         scroll_x = Scrollbar(record_frame, orient=HORIZONTAL)
#         scroll_y = Scrollbar(record_frame, orient=VERTICAL)

#         self.student_table = ttk.Treeview(
#             record_frame,
#             columns=("id", "name", "department", "roll", "email", "phone", "address", "gender", "dob"),
#             xscrollcommand=scroll_x.set,
#             yscrollcommand=scroll_y.set,
#             show='headings'
#         )
#         scroll_x.config(command=self.student_table.xview)
#         scroll_y.config(command=self.student_table.yview)
#         scroll_x.pack(side=BOTTOM, fill=X)
#         scroll_y.pack(side=RIGHT, fill=Y)

#         # Define headings and fixed-width columns
#         for col in self.student_table["columns"]:
#             self.student_table.heading(col, text=col.title())
#             self.student_table.column(col, width=150, stretch=False)  # Fixed width, no auto shrink

#         self.student_table.pack(side=LEFT, fill=BOTH, expand=True)
#         self.student_table.bind("<ButtonRelease-1>", self.load_selected_record)

#         self.fetch_records()

#     def exit_fullscreen(self):
#         self.root.attributes('-fullscreen', False)
#         self.root.geometry("1351x800") 

#     def add_data(self):
#         try:
#             if self.var_name.get() == "" or self.var_roll.get() == "":
#                 messagebox.showerror("Error", "Name and Roll No are required!", parent=self.root)
#                 return

#             try:
#                 roll_int = int(self.var_roll.get())
#             except ValueError:
#                 messagebox.showerror("Error", "Roll No must be an integer!", parent=self.root)
#                 return

#             conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
#             cursor = conn.cursor()

#             if hasattr(self, "editing_id"):
#                 update_query = """
#                     UPDATE students SET name=%s, department=%s, roll=%s, email=%s, phone=%s, address=%s, gender=%s, dob=%s
#                     WHERE id=%s
#                 """
#                 data = (
#                     self.var_name.get(), self.var_dept.get(), roll_int, self.var_email.get(),
#                     self.var_phone.get(), self.var_address.get(), self.var_gender.get(), self.var_dob.get(), self.editing_id
#                 )
#                 cursor.execute(update_query, data)
#                 messagebox.showinfo("Success", "Student data updated successfully!", parent=self.root)
#                 del self.editing_id
#             else:
#                 query = """
#                     INSERT INTO students (name, department, roll, email, phone, address, gender, dob)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                 """
#                 data = (
#                     self.var_name.get(), self.var_dept.get(), roll_int, self.var_email.get(),
#                     self.var_phone.get(), self.var_address.get(), self.var_gender.get(), self.var_dob.get()
#                 )
#                 cursor.execute(query, data)
#                 messagebox.showinfo("Success", f"Student data saved successfully!\nGenerated ID: {cursor.lastrowid}", parent=self.root)

#             conn.commit()
#             conn.close()
#             self.reset_fields()
#             self.fetch_records()

#         except pymysql.err.IntegrityError:
#             messagebox.showerror("Duplicate", "Roll No already exists.", parent=self.root)
#         except pymysql.MySQLError as err:
#             messagebox.showerror("DB Error", f"MySQL Error: {str(err)}", parent=self.root)
#         except Exception as e:
#             messagebox.showerror("Error", f"Unexpected Error: {str(e)}", parent=self.root)

#     def fetch_records(self):
#         conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, name, department, roll, email, phone, address, gender, dob FROM students")
#         rows = cursor.fetchall()
#         self.student_table.delete(*self.student_table.get_children())
#         for row in rows:
#             self.student_table.insert('', END, values=row)
#         conn.close()

#     def load_selected_record(self, event):
#         selected = self.student_table.focus()
#         values = self.student_table.item(selected, 'values')
#         if not values:
#             return
#         student_id = values[0]
#         conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM students WHERE id=%s", (student_id,))
#         record = cursor.fetchone()
#         conn.close()

#         if record:
#             self.editing_id = record[0]
#             self.var_name.set(record[1])
#             self.var_dept.set(record[2])
#             self.var_roll.set(record[3])
#             self.var_email.set(record[4])
#             self.var_phone.set(record[5])
#             self.var_address.set(record[6])
#             self.var_gender.set(record[7])
#             self.var_dob.set(record[8])

#     def reset_fields(self):
#         self.var_name.set("")
#         self.var_dept.set("")
#         self.var_roll.set("")
#         self.var_email.set("")
#         self.var_phone.set("")
#         self.var_address.set("")
#         self.var_gender.set("")
#         self.var_dob.set("")

#     def cancel_edit(self):
#         self.reset_fields()
#         if hasattr(self, "editing_id"):
#             del self.editing_id
#         messagebox.showinfo("Cancelled", "Edit cancelled. Back to Add mode.")

#     def search_record(self):
#         search_term = self.var_search.get()
#         conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, name, department, roll, email, phone, address, gender, dob FROM students WHERE name LIKE %s OR department LIKE %s OR roll LIKE %s",
#                        (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
#         rows = cursor.fetchall()
#         self.student_table.delete(*self.student_table.get_children())
#         for row in rows:
#             self.student_table.insert('', END, values=row)
#         conn.close()

#     def delete_record(self):
#         if not hasattr(self, "editing_id"):
#             messagebox.showwarning("No Selection", "Please select a student to delete.", parent=self.root)
#             return

#         confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?", parent=self.root)
#         if confirm:
#             try:
#                 conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
#                 cursor = conn.cursor()
#                 cursor.execute("DELETE FROM students WHERE id=%s", (self.editing_id,))
#                 conn.commit()
#                 conn.close()

#                 messagebox.showinfo("Deleted", "Record deleted successfully.", parent=self.root)
#                 self.reset_fields()
#                 if hasattr(self, "editing_id"):
#                     del self.editing_id
#                 self.fetch_records()
#             except pymysql.MySQLError as err:
#                 messagebox.showerror("DB Error", f"MySQL Error: {str(err)}", parent=self.root)

#     def go_to_main(self):
#         self.root.destroy()
#         os.system("python main_ui.py")

# if __name__ == "__main__":
#     root = Tk()
#     app = StudentDetails(root)
#     root.mainloop()

from tkinter import *
from tkinter import messagebox, ttk
import pymysql
import os

class StudentDetails:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.title("Student Details")
        self.root.configure(bg="#0A192F")

        # Variables
        self.var_name = StringVar()
        self.var_dept = StringVar()
        self.var_roll = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_search = StringVar()

        # Title
        title_lbl = Label(self.root, text="STUDENT DETAILS", font=("Arial", 24, "bold"), bg="#0A192F", fg="#00FFFF")
        title_lbl.pack(pady=20)

        # Input Frame
        input_frame = Frame(self.root, bg="#112240", bd=2, relief=RIDGE)
        input_frame.place(x=30, y=100, width=600, height=600)

        labels = [
            ("Name", self.var_name),
            ("Department", self.var_dept),
            ("Roll No", self.var_roll),
            ("Email", self.var_email),
            ("Phone", self.var_phone),
            ("Address", self.var_address),
            ("Gender", self.var_gender),
            ("DOB (YYYY-MM-DD)", self.var_dob),
        ]

        for i, (text, var) in enumerate(labels):
            Label(input_frame, text=text, font=("Arial", 12, "bold"), bg="#112240", fg="white").grid(row=i, column=0, padx=10, pady=10, sticky=W)
            Entry(input_frame, textvariable=var, font=("Arial", 12), width=25).grid(row=i, column=1, padx=10, pady=10)

        # Button Frame
        btn_frame = Frame(input_frame, bg="#112240")
        btn_frame.place(x=10, y=480, width=570, height=90)

        Button(btn_frame, text="Save", command=self.add_data, width=12, font=("Arial", 12, "bold"), bg="#00FFFF", fg="black").grid(row=0, column=0, padx=5, pady=5)
        Button(btn_frame, text="Reset", command=self.reset_fields, width=12, font=("Arial", 12, "bold"), bg="orange", fg="black").grid(row=0, column=1, padx=5, pady=5)
        Button(btn_frame, text="Cancel Edit", command=self.cancel_edit, width=12, font=("Arial", 12, "bold"), bg="#FFC107", fg="black").grid(row=0, column=2, padx=5, pady=5)
        Button(btn_frame, text="Delete", command=self.delete_record, width=12, font=("Arial", 12, "bold"), bg="#FF4C4C", fg="white").grid(row=0, column=3, padx=5, pady=5)
        Button(btn_frame, text="Delete All", command=self.delete_all_records, width=12, font=("Arial", 12, "bold"), bg="#8B0000", fg="white").grid(row=1, column=0, padx=5, pady=5)
        Button(btn_frame, text="Back", command=self.go_to_main, width=12, font=("Arial", 12, "bold"), bg="red", fg="white").grid(row=1, column=1, columnspan=3, pady=5)

        # Table Frame for records
        record_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#112240")
        record_frame.place(x=650, y=100, width=690, height=600)

        Entry(record_frame, textvariable=self.var_search, font=("Arial", 12)).pack(pady=5)
        Button(record_frame, text="Search", command=self.search_record, bg="#00FFFF", font=("Arial", 12)).pack(pady=5)

        scroll_x = Scrollbar(record_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(record_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            record_frame,
            columns=("id", "name", "department", "roll", "email", "phone", "address", "gender", "dob"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            show='headings'
        )
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        for col in self.student_table["columns"]:
            self.student_table.heading(col, text=col.title())
            self.student_table.column(col, width=150, stretch=False)

        self.student_table.pack(side=LEFT, fill=BOTH, expand=True)
        self.student_table.bind("<ButtonRelease-1>", self.load_selected_record)

        self.fetch_records()

    def exit_fullscreen(self):
        self.root.attributes('-fullscreen', False)
        self.root.geometry("1351x800") 

    def add_data(self):
        try:
            if self.var_name.get() == "" or self.var_roll.get() == "":
                messagebox.showerror("Error", "Name and Roll No are required!", parent=self.root)
                return

            try:
                roll_int = int(self.var_roll.get())
            except ValueError:
                messagebox.showerror("Error", "Roll No must be an integer!", parent=self.root)
                return

            conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
            cursor = conn.cursor()

            if hasattr(self, "editing_id"):
                update_query = """
                    UPDATE students SET name=%s, department=%s, roll=%s, email=%s, phone=%s, address=%s, gender=%s, dob=%s
                    WHERE id=%s
                """
                data = (
                    self.var_name.get(), self.var_dept.get(), roll_int, self.var_email.get(),
                    self.var_phone.get(), self.var_address.get(), self.var_gender.get(), self.var_dob.get(), self.editing_id
                )
                cursor.execute(update_query, data)
                messagebox.showinfo("Success", "Student data updated successfully!", parent=self.root)
                del self.editing_id
            else:
                query = """
                    INSERT INTO students (name, department, roll, email, phone, address, gender, dob)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = (
                    self.var_name.get(), self.var_dept.get(), roll_int, self.var_email.get(),
                    self.var_phone.get(), self.var_address.get(), self.var_gender.get(), self.var_dob.get()
                )
                cursor.execute(query, data)
                messagebox.showinfo("Success", f"Student data saved successfully!\nGenerated ID: {cursor.lastrowid}", parent=self.root)

            conn.commit()
            conn.close()
            self.reset_fields()
            self.fetch_records()

        except pymysql.err.IntegrityError:
            messagebox.showerror("Duplicate", "Roll No already exists.", parent=self.root)
        except pymysql.MySQLError as err:
            messagebox.showerror("DB Error", f"MySQL Error: {str(err)}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected Error: {str(e)}", parent=self.root)

    def fetch_records(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, department, roll, email, phone, address, gender, dob FROM students")
        rows = cursor.fetchall()
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert('', END, values=row)
        conn.close()

    def load_selected_record(self, event):
        selected = self.student_table.focus()
        values = self.student_table.item(selected, 'values')
        if not values:
            return
        student_id = values[0]
        conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id=%s", (student_id,))
        record = cursor.fetchone()
        conn.close()

        if record:
            self.editing_id = record[0]
            self.var_name.set(record[1])
            self.var_dept.set(record[2])
            self.var_roll.set(record[3])
            self.var_email.set(record[4])
            self.var_phone.set(record[5])
            self.var_address.set(record[6])
            self.var_gender.set(record[7])
            self.var_dob.set(record[8])

    def reset_fields(self):
        self.var_name.set("")
        self.var_dept.set("")
        self.var_roll.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_gender.set("")
        self.var_dob.set("")

    def cancel_edit(self):
        self.reset_fields()
        if hasattr(self, "editing_id"):
            del self.editing_id
        messagebox.showinfo("Cancelled", "Edit cancelled. Back to Add mode.")

    def search_record(self):
        search_term = self.var_search.get()
        conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, department, roll, email, phone, address, gender, dob FROM students WHERE name LIKE %s OR department LIKE %s OR roll LIKE %s",
                       (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert('', END, values=row)
        conn.close()

    def delete_record(self):
        if not hasattr(self, "editing_id"):
            messagebox.showwarning("No Selection", "Please select a student to delete.", parent=self.root)
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?", parent=self.root)
        if confirm:
            try:
                conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id=%s", (self.editing_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Deleted", "Record deleted successfully.", parent=self.root)
                self.reset_fields()
                if hasattr(self, "editing_id"):
                    del self.editing_id
                self.fetch_records()
            except pymysql.MySQLError as err:
                messagebox.showerror("DB Error", f"MySQL Error: {str(err)}", parent=self.root)

    def delete_all_records(self):
        confirm = messagebox.askyesno("Confirm Delete All", "This will delete all student records and reset ID. Are you sure?", parent=self.root)
        if confirm:
            try:
                conn = pymysql.connect(host="localhost", user="root", password="", database="fac", port=3306)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students")
                cursor.execute("ALTER TABLE students AUTO_INCREMENT = 1")
                conn.commit()
                conn.close()
                self.fetch_records()
                self.reset_fields()
                messagebox.showinfo("Deleted", "All records deleted and ID reset to 1.", parent=self.root)
            except pymysql.MySQLError as err:
                messagebox.showerror("DB Error", f"MySQL Error: {str(err)}", parent=self.root)

    def go_to_main(self):
        self.root.destroy()
        os.system("python main_ui.py")

if __name__ == "__main__":
    root = Tk()
    app = StudentDetails(root)
    root.mainloop()
