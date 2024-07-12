from database_module import connect_to_db
import tkinter as tk
from tkinter import ttk

class Admin:
    def __init__(self, check_table):
        self.check_table = check_table
 
    def execute(self, query):
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        
        except Exception as e:
            return None
        
    def table_details(self):
        if self.check_table == 1:
            query = '''SELECT * FROM student_details'''
        elif self.check_table == 2:
            query = '''SELECT * FROM student_grades'''
        elif self.check_table == 3:
            query = '''SELECT * FROM teacher_details'''
        return self.execute(query)


class Admin_GUI(Admin):
    def __init__(self):
        self.data_gui = tk.Tk()
        self.data_gui.geometry('700x500+400+200')
        self.data_gui.title('Data Admin System')
        self.show_data()

    def show_data(self):       
        tk.Label(self.data_gui, text='1.Student details   2.Student Grades   3. Teacher Details').pack()                
        # Table 1: Student details
        show_data = Admin(1)
        check_table = show_data.table_details()

        if check_table is not None:
            tree = ttk.Treeview(self.data_gui, columns=('Student ID', 'Student Name', 'Username', 'Password'), show='headings')
            tree.pack()

            tree.heading('Student ID', text='Student ID')
            tree.heading('Student Name', text='Student Name')
            tree.heading('Username', text='Username')
            tree.heading('Password', text='Password')

            style = ttk.Style()
            style.configure("Treeview", rowheight=30, borderwidth=0)
            for col in ('Student ID', 'Student Name', 'Username', 'Password'):
                tree.column(col, anchor='center', width=100)

            for row in check_table:
                tree.insert('', 'end', values=row)
        
        # Table 2: Student details
        show_data2 = Admin(2)
        check_table2 = show_data2.table_details()

        if check_table2 is not None:
            tree2 = ttk.Treeview(self.data_gui, columns=('Student Name', 'Course Code', 'Course Name',
                                                        'Course Teacher', 'Score', 'Grade'), show='headings')
            tree2.pack()
            tree2.heading('Student Name', text='Student Name')
            tree2.heading('Course Code', text='Course Code')
            tree2.heading('Course Name', text='Course Name')
            tree2.heading('Course Teacher', text='Course Teacher')
            tree2.heading('Score', text='Score')
            tree2.heading('Grade', text='Grade')


            style = ttk.Style()
            style.configure("Treeview", rowheight=30, borderwidth=0)
            for col in ('Student Name', 'Course Code', 'Course Name','Course Teacher', 'Score', 'Grade'):
                tree2.column(col, anchor='center', width=100)

            for row in check_table2:
                tree2.insert('', 'end', values=row)

        # Table 3 Teacher Details
        show_data3 = Admin(3)
        check_table3 = show_data3.table_details()

        if check_table3 is not None:
            tree3 = ttk.Treeview(self.data_gui, columns=('Teacher Name', 'Teacher Password'), show='headings')
            tree3.pack()
            tree3.heading('Teacher Name', text='Teacher Name')
            tree3.heading('Teacher Password', text='Teacher Password')
            style = ttk.Style()
            style.configure("Treeview", rowheight=30, borderwidth=0)
            for col in ('Teacher Name', 'Teacher Password'):
                tree3.column(col, anchor='center', width=100)

            for row in check_table3:
                tree3.insert('', 'end', values=row)

        tree.place(x=150, y=50, width=400, height=125)
        tree2.place(x=150, y=200, width=400, height=150)
        tree3.place(x=150, y=380,width=400, height=100)


if __name__ == "__main__":
    admin_app = Admin_GUI()
    admin_app.data_gui.mainloop()