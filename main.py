from database_sys import *

##>>>>>>>>>>>>>>  main menu provide 5 other menus for each class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def main_menu():
    while True:
        print("\n<<<<<  WELCOME TO THE SCHOOL SYSTEM  >>>>>")
        print("xX=========== Main Menu ===========Xx")
        print("\n1. Manage Classes")
        print("2. Manage Students")
        print("3. Manage Teachers")
        print("4. Manage Courses")
        print("5. Generate Reports and Visualization")
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
            print("ok...Exiting the program.... bye bye o(╥﹏╥) !")
            break
        else:
            print("womp womp ! Invalid choice! try valid options ! ! ")

#>>>>>>>>>>>>>>>>..........................................CLASS MENU................................            
def class_menu():
    while True:
        print("\n=====> Class Management <=====")
        print("\n1. Add a New Class")
        print("2. Update Class Details")
        print("3. Delete a Class")
        print("4. Show All Classes")
        print("5. Search for a Class")
        print("6. Back to Main Menu")
        #>......................................ADD CLASS
        choice = input("Enter your choice: ")
        if choice == "1":
            class_id = input("Enter an ID for the Class: ")
            class_name = input("Enter Class Name: ")
            class_capacity = int(input("Enter Class Capacity: "))
            try:
               C = Class(dbb ,class_id, class_name, class_capacity)
               C.add_class()
            except ValueError as e:
                print(e)
         #>......................................EDIT CLASS       
        elif choice == "2":
            class_id =input("Enter The class ID that you want to Update:")
            field = input("Enter The field To Update:")
            value =input("Enter The new Value :")
            try:   
                 C = Class(dbb , class_id, "" , 0 )
                 C.edit_class(class_id , field, value)
            except ValueError as e: 
                print(e) 
          #>........................................REMOVE CLASS        
        elif choice == "3":
            class_id = input("Enter The class ID to delete:")
            try:
               C = Class(dbb , class_id, "" , 0 )
               C.remove_class(class_id)
            except ValueError as e :
                print(e)   
           #>........................................DISPLAY CLASSES TABLE
        elif choice == "4":           
            query = "SELECT * FROM classes"
            result = dbb.execute_query(query, fetch=True)
            if result:
                for row in result:
                  print(row)
         #>..........................................SEARCH 
        elif choice == "5":
            class_id=input("Enter the class ID to search:")
            C= Class(dbb , class_id , "" , 0)
            C.search_class(class_id)

         #>.........................................BACK TO MAIN MENU 
        elif choice == "6":
            break
        else:
            print("womp womp ! Invalid choice!")
          
  #>>>>>>>>>>>.........................................STUDENT MENU........................................          
def student_menu():
    while True:
        print("\n=====> Student Management <=====")
        print("\n1. Add a New Student")
        print("2. Update Student Details")
        print("3. Delete a Student")
        print("4. Show All Students")
        print("5. Search for a Student")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")
      #>>>>>>...............................ADD STUDENT  
        if choice == "1":
            name =input("Enter Student name:")
            grade = input("Enter student Grade:")
            email = input("Enter student Email:")
            age = input("Enter Student Age :")
            class_id =input("Enter Student class ID")
            
            
        #>>>>....................................EDIT STUDENT
        elif choice == "2":
            pass
        #>>>>>......................................REMOVE STUDENT
        elif choice == "3":
            pass
        #>>>>>>.......................................DISPLAY STUDENTS TABLE
        elif choice == "4":
            pass
        #>>>>>>..........................................SEARCH
        elif choice == "5":
            pass
        ####...................BACK
        elif choice == "6":
            break
        else:
            print("Invalid choice! Womp Womp !!!!!!!!")
            
  #>>>>>>>>>>>>>>.............TEACHER MENU          
def teacher_menu():
    while True:
        print("\n=====> Teacher Management <=====")
        print("\n1. Add a New Teacher")
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
        print("\n=====> Course Management <=====")
        print("\n1. Add a New Course")
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
        print("\n=====> Reports and Visualization <=====")
        print("\n1. View Class-wise Student List")
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
            
#############################################################################################
if __name__ == "__main__":
    logger = Logger()
    dbb = DB_connection("root" , "Bita1380" , "localhost" , "school_sys", logger)
    try:
        main_menu()  
        
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        dbb.close()              
            

