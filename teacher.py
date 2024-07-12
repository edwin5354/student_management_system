from database_module import connect_to_db
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TeacherInterface:
    def __init__(self, teacher, password):
        self.teacher = teacher
        self.password = password
        self.students = []

    def execute(self, query, placehold_var):
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute(query, placehold_var)
            var_result = cursor.fetchall()
            cursor.close()
            connection.close()
            return var_result
        
        except Exception as e:
            return None
    
    def teacher_detail(self):
        query = ''' SELECT teacher_name, teacher_password FROM teacher_details
        WHERE teacher_name = %s AND teacher_password = %s;
        '''
        placehold_var = (self.teacher, self.password)

        return self.execute(query, placehold_var)
    
    def credentials(self):
        teacher_val = self.teacher_detail()
        if teacher_val:
            return True
        else:
            return None
        
    def show_student_name(self):
        query = ''' SELECT student_name FROM student_details;'''        
        student = self.execute(query, None)
        self.students.append(student)
        self.student_list = ' '.join([name[0] for sublist in self.students for name in sublist])

        return self.student_list
    

class Teacher_GUI():
    def __init__(self):
        self.teacher_name = ''
        self.student_name = ''
        self.course_name = ''
        self.teacher_page()

    def teacher_verify(self):
        self.course_input = TeacherInterface(teacher=self.teacher_entry.get(), 
                                             password=self.password_entry.get())
        if self.course_input.credentials():
                self.teacher_name = self.teacher_entry.get()
                self.marking_interface()

        else:
            messagebox.showerror('Error', 'Invalid login credentials. Please try again.')

    def marking_interface(self):
        self.teacher_login.destroy()
        self.mark_assign = tk.Tk()
        self.mark_assign.geometry('700x300+400+200') 
        self.mark_assign.title('Marking System')
        self.course_input.show_student_name()
        tk.Label(self.mark_assign, text= '\nPlease select a student that you want to grade.\n').pack()
        self.selected_student = tk.StringVar()
        self.combo_box = ttk.Combobox(self.mark_assign, textvariable= self.selected_student, value= self.course_input.student_list)
        self.combo_box.bind('<<ComboboxSelected>>', self.store_student_name)
        self.combo_box.pack()

    def store_student_name(self, event=None):
        self.student_name = self.combo_box.get()
        self.subject_page(event)
    
    def store_course_name(self, event=None):
        self.course_name = self.mark_course.get()
        self.mark_page(event)

    def mark_page(self, event): 
        self.subject_interface.destroy()
        self.score_interface = tk.Tk()
        self.score_interface.geometry('700x300+400+200') 
        self.score_interface.title('Marking System')
        tk.Label(self.score_interface, text = 'Access Granted. Please grade the following assignment.').pack()
        tk.Label(self.score_interface, text = 'Score: 0 - 100').pack()
        self.score_entry = tk.Entry(self.score_interface)
        self.score_entry.pack()

        score_button = tk.Button(self.score_interface, text= 'Submit Score', command=self.update_grade)
        score_button.pack()

        self.return_button = tk.Button(self.score_interface, text='return', command=self.return_homepage).pack()

    def show_subject(self):
        course_list = []
        query =  '''SELECT course_name FROM student_grades
        WHERE student_name = %s;
        '''
        placehold_var = (self.selected_student.get(),)

        all_courses = self.course_input.execute(query, placehold_var)
        for course in all_courses:
            course_list.append(course[0])

        return course_list

    def subject_page(self, event):
        self.mark_assign.destroy()
        self.subject_interface = tk.Tk()
        self.subject_interface.geometry('700x300+400+200') 
        self.subject_interface.title('Marking System')

        student_courses = self.show_subject() 
        tk.Label(self.subject_interface, text="\nHere is the student's enrolled course(s)\n").pack()
        self.mark_course = tk.StringVar()
        combo_box = ttk.Combobox(self.subject_interface, textvariable= self.mark_course, value= student_courses)
        combo_box.bind('<<ComboboxSelected>>', self.store_course_name)
        combo_box.pack()

    def update_grade(self):
        score_input = int(self.score_entry.get())
        if 0 <= score_input <= 100:
            updated_records = self.update_score_records(score=score_input)
            key = ['Student Name', 'Course Code', 'Subject', 
               'Assigned Teacher', 'Score', 'Grade']
            value = [element for i in updated_records for element in i]
            my_dict = dict(zip(key, value))

            tk.Label(self.score_interface, text="").pack()

            for key, value in my_dict.items():
                tk.Label(self.score_interface, text=f"{key}: {value}").pack()

        else:
            messagebox.showerror('Error', 'Invalid Score. Please enter a number between 0 and 100.')

    def teacher_page(self):
        self.teacher_login = tk.Tk()
        self.teacher_login.geometry('700x300+400+200') 
        self.teacher_login.title('Teacher Login System')

        tk.Label(self.teacher_login, text= 'Your Name').pack()
        self.teacher_entry = tk.Entry(self.teacher_login)
        self.teacher_entry.pack()
    
        tk.Label(self.teacher_login, text= 'password').pack()
        self.password_entry = tk.Entry(self.teacher_login, show= '*')
        self.password_entry.pack()

        self.teacher_login_but = tk.Button(self.teacher_login, text='Teacher Login', command=self.teacher_verify)
        self.teacher_login_but.pack()    
    
    def update_score_records(self, score):
        try:
            connection = connect_to_db()
            cursor = connection.cursor()

            update_query = '''UPDATE student_grades SET course_teacher = %s, score = %s, grade = %s
            WHERE course_name = %s AND student_name = %s;'''

            grade = self.insert_grades(score)
            placehold_var = (self.teacher_name, score, grade, self.course_name, self.student_name)
        
            # Update the row
            cursor.execute(update_query, placehold_var)
            connection.commit()

            select_query = '''SELECT * FROM student_grades WHERE course_name = %s AND student_name = %s;'''

            # Fetch and display the updated records
            cursor.execute(select_query, (self.course_name, self.student_name,))
            updated_records = cursor.fetchall()
            cursor.close()
            connection.close()

            return updated_records
        
        except Exception as e:
            return None

    def insert_grades(self, score):
        if score >= 85:
            return 'HD'
        elif 75 <= score < 85:
            return 'DI' 
        elif 65 <= score < 75:
            return 'CR' 
        elif 50 <= score < 65:
            return 'PS'
        else:
            return 'FA' 

    def return_homepage(self):
        if self.score_interface:
            self.score_interface.destroy()
        self.teacher_page()


if __name__ == "__main__":
    teacher_app = Teacher_GUI()
    teacher_app.teacher_login.mainloop()