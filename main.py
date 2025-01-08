from database_sys import *

##>>>>>>>>>>>>>>  main menu provide 5 other menus for each class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main_menu():
    while True:
        print("\n===== Main Menu =====")
        print("1. Manage Classes")
        print("2. Manage Students")
        print("3. Manage Teachers")
        print("4. Manage Courses")
        print("5. Generate Reports")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            class_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            teacher_menu()
        elif choice == "4":
            course_menu()
        elif choice == "5":
            report_menu()
        elif choice == "6":
            print("Exiting the program.... bye bye (ó﹏ò｡)!")
            break
        else:
            print("womp womp ! Invalid choice! try valid options ! ! ")

#>>>>>>>>>>>>>>>>......CLASS MENU            
def class_menu():
    while True:
        print("\n===== Class Management =====")
        print("1. Add a New Class")
        print("2. Update Class Details")
        print("3. Delete a Class")
        print("4. Show All Classes")
        print("5. Search for a Class")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            break
        else:
            print("womp womp ! Invalid choice!")
          
  #>>>>>>>>>>>..............STUDENT MENU          
def student_menu():
    while True:
        print("\n===== Student Management =====")
        print("1. Add a New Student")
        print("2. Update Student Details")
        print("3. Delete a Student")
        print("4. Show All Students")
        print("5. Search for a Student")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            break
        else:
            print("Invalid choice! Womp Womp !!!!!!!!")
            
  #>>>>>>>>>>>>>>.............TEACHER MENU          
def teacher_menu():
    while True:
        print("\n===== Teacher Management =====")
        print("1. Add a New Teacher")
        print("2. Update Teacher Details")
        print("3. Delete a Teacher")
        print("4. Show All Teachers")
        print("5. Search for a Teacher")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            break
        else:
            print("Invalid choice! Please try agai ! ! womp")
            
   #>>>>>>>>>........COURSE MENU         
def course_menu():
    while True:
        print("\n===== Course Management =====")
        print("1. Add a New Course")
        print("2. Update Course Details")
        print("3. Delete a Course")
        print("4. Show All Courses")
        print("5. Search for a Course")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            break
        else:
            print("Invalid choice! use valid choices !!!!!")
            
   #>>>>>>>>>>>>>>>>>.......... REPORT MENU         
def report_menu():
    while True:
        print("\n===== Reports =====")
        print("1. View Class-wise Student List")
        print("2. View Teacher Assignments")
        print("3. View Course Enrollments")
        print("4. Generate Summary Report")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            break
        else:
            print("Invalid choice! choose Valid Options !!!")

            
            

