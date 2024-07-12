from database_module import connect_to_db
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Student:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.courses = []

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
    
    def enrol_new_courses(self):
        pass

    
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