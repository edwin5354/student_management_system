from database_module import connect_to_db
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Student:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def execute(self, query, placehold_var):
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute(query, placehold_var)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        
        except Exception as e:
            return None
        
    def login_details(self):
        query =  '''SELECT student_name, username, student_password FROM student_details WHERE 
        username = %s AND student_password = %s
        '''
        placehold_var = (self.username, self.password)
        return self.execute(query, placehold_var)        
    
    def check_credentials(self):
        login_val = self.login_details()
        if login_val:
            return True
        else:
            return None
    
    def course_grade(self):
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT course_code, course_name, score, grade
        FROM student_grades WHERE student_name = %s;
        ''', (self.name,))
        course_details = cursor.fetchall()
        cursor.close()
        connection.close()  
        return course_details
    
    def enroll_new_courses(self):
        query = '''SELECT DISTINCT course_name FROM student_grades WHERE course_name NOT IN 
            (SELECT course_name FROM student_grades WHERE student_name = %s) AND course_name IN 
            (SELECT course_name FROM student_grades WHERE student_name != %s)'''
        
        placehold_var = (self.name, self.name)
        return self.execute(query, placehold_var)


class Student_GUI:
    def __init__(self):
        self.homepage()
        
    def homepage(self):
        self.login_window = tk.Tk()
        self.login_window.geometry('700x300+400+200') 
        self.login_window.title('Student Management System')

        tk.Label(self.login_window, text='Student Name').pack()
        self.name_entry = tk.Entry(self.login_window)
        self.name_entry.pack()

        tk.Label(self.login_window, text='Username').pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()

        tk.Label(self.login_window, text='Password').pack()
        self.password_entry = tk.Entry(self.login_window, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_window, text='Student login', command=self.verify_student)
        self.login_button.pack()

    def show_report(self):
        self.login_window.destroy()
        self.report_window = tk.Tk()
        self.report_window.geometry('700x300+400+200')
        self.report_window.title('Student Management System')

        tree = ttk.Treeview(self.report_window, columns=('Course Code', 'Course Name', 'Score', 'Grade'), show='headings')
        tree.pack()

        report_check = self.student_input.course_grade()

        tree.heading('Course Code', text='Course Code')
        tree.heading('Course Name', text='Course Name')
        tree.heading('Score', text='Score')
        tree.heading('Grade', text='Grade')

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, borderwidth=0)
        for col in ('Course Code', 'Course Name', 'Score', 'Grade'):
            tree.column(col, anchor='center', width=100)

        for row in report_check:
            tree.insert('', 'end', values=row)

        tree.place(x=125,y=100,width=450,height=125)

        tk.Label(self.report_window, text=f'Welcome! Here is your Scorecard.\n').pack()
        self.return_button = tk.Button(self.report_window, text='return', command=self.return_homepage).pack()

        tk.Label(self.report_window, text= '\nWant to enroll a new course? Click Here.\n').place(x=125,y=230)
        tk.Button(self.report_window, text='Register', command= self.register_page).place(x=350, y=240)

    def register_page(self):
        self.report_window.destroy()
        self.register_window = tk.Tk()
        self.register_window.geometry('700x300+400+200')
        self.register_window.title('Student Management System')
        tk.Label(self.register_window, text='Here are the available courses that you may enroll.\n').pack()
        course_availability = self.student_input.enroll_new_courses()
        course_availability_list = [name for sublist in course_availability for name in sublist]
        self.enrolled_course = tk.StringVar()
        self.course_box = ttk.Combobox(self.register_window, textvariable= self.enrolled_course, value= course_availability_list)
        self.course_box.bind('<<ComboboxSelected>>', self.store_enrolled_course)
        self.course_box.pack()

    def store_enrolled_course(self, event):
        self.selected_course = self.course_box.get()
        tk.Label(self.register_window, text='\nCourse enrolled! Please Log in again to see your updated scorecard details.\n').pack()
        tk.Label(self.register_window, text='A teacher will grade your assignments once you enroll in the course.').pack()
        self.add_course()
    
    def get_code(self):
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT course_code FROM student_grades WHERE course_name = %s;
        ''', (self.selected_course,))
        update_details = cursor.fetchall()
        cursor.close()
        connection.close()  
        return [code for code in update_details[0]][0]
    
    def add_course(self):
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO student_grades (student_name, course_code, course_name)
        VALUES (%s, %s, %s);
        ''', (self.student_input.name, self.get_code() ,self.selected_course))
        insert_details = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()  
        return insert_details        

    def return_homepage(self):
        if self.report_window:
            self.report_window.destroy()
        self.homepage()

    def verify_student(self):
        self.student_input = Student(name = self.name_entry.get(), username= self.username_entry.get(), 
                                password=self.password_entry.get())
        if self.student_input.check_credentials():
            self.show_report()
        else:
            messagebox.showerror('Error', 'Invalid login credentials. Please try again.')


if __name__ == "__main__":
    student_app = Student_GUI()
    student_app.login_window.mainloop()
