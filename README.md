Assalam o Alikum Warahmatullahi Wabarakatuhu, All praises to Allah S.W.T by his permission and help i'm able to complete this program.
Its my final year project related to my college attendence system. how it works ? 

1) First we make a record for a student/person from student detail module(form).
2) Then it create a dataset images of a person/student from photo module (based on student Roll No) using web cam of the laptop.  (in my case 50 images in 3 secs).
3) Then it train on that dataset images using train data module (based on student/person Roll No) using Algorithum called Local Binary Patterns Histogram (LBPH).
4) After that it detect the person/student using face recognition module using Algorithm called Haar Cascade Classifier.
5) If it detects the student/person then automattically it marks the attendence of that particular person/student.

Now what do you require after cloning this repo...
1) create a database (in my case 'fac').
2) create three tables (in my case 'admin_credentials', 'students', 'attendence').
3) in admin_credential table i have Three columns 'id', 'username', 'password'.
4) in my students table i have Eleven columns 'id', 'name', 'department', 'roll', 'email', 'phone', 'address', 'gender', 'dob', 'pictures', 'train_data'.
5) in my attendence table i have Five columns 'roll', 'name', 'department', 'status', 'timestamp'. 

I'm a beginner so im sure that there are some tweaks need to do with this program. Jazakallah Khair
