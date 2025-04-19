import sqlite3

# conn = sqlite3.connect("students.db")
# cursor = conn.cursor()

# # Check if 'roll_no' column already exists
# cursor.execute("PRAGMA table_info(student_details)")
# columns = [col[1] for col in cursor.fetchall()]

# if "roll_no" not in columns:
#     cursor.execute("ALTER TABLE student_details ADD COLUMN roll_no TEXT")
#     conn.commit()
#     print("Column 'picture' added successfully!")
# else:
#     print("Column 'picture' already exists.")

# conn.close()


conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(student_details);")
columns = cursor.fetchall()
for col in columns:
    print(col)

conn.close()

# import sqlite3
# print("SQLite version:", sqlite3.version)
# print("SQLite library version:", sqlite3.sqlite_version)
