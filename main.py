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

        choice = input("\nEnter your choice: ")
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
        choice = input("\nEnter your choice: ")
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
            class_id =input("Enter The class ID that you want to Update: ")
            field = input("Enter The field To Update: ")
            value =input("Enter The new Value: ")
            try:  
                 if field == "class_capacity":
                    value = int(value)
                     
                 C = Class(dbb , class_id, "" , 0 )
                 C.edit_class(class_id , field, value)
                 
            except ValueError as e: 
                print(e) 
          #>........................................REMOVE CLASS        
        elif choice == "3":
            class_id = input("Enter The class ID to delete: ")
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
                print("\nAll Classes: ")
                for row in result:
                  print(row)
            else :
                print("No Class Found !")      
         #>..........................................SEARCH 
        elif choice == "5":
            class_id=input("Enter the class ID to search: ")
            C= Class(dbb , class_id , "" , 0)
            C.search_class(class_id)

         #>.........................................BACK TO MAIN MENU 
        elif choice == "6":
            break
        else:
            print("womp womp ! Invalid choice!")
          
  #>>>>>>>>>>>......................>>>>>>>>>>>   STUDENT MENU   ....<<<<<<<<<<<<<<<<<<<<...................          
def student_menu():
    while True:
        print("\n=====> Student Management <=====")
        print("\n1. Add a New Student")
        print("2. Update Student Details")
        print("3. Delete a Student")
        print("4. Show All Students")
        print("5. Search for a Student")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ")
      #>>>>>>...............................ADD STUDENT  
        if choice == "1":
            name =input("Enter Student name: ")
            age = int(input("Enter Student Age: "))
            email = input("Enter student Email:")
            grade = int(input("Enter student Grade: "))
            class_id =input("Enter Student class ID: ")
            try :
                S = Student(dbb , name, grade, email, age  ,class_id)
                S.add_stu()
            except ValueError as e :
               print(e)
            
        #>>>>....................................EDIT STUDENT
        elif choice == "2":
            Student_id =input("Enter The Student ID: ")
            field = input("Enter The field To Update: ")
            value =input("Enter The new Value:")
            try:   
                 S = Student(dbb , "", 0, "" , 0 ,"")
                 S.edit_stu(Student_id , field, value)
            except ValueError as e: 
                print(e)
        #>>>>>......................................REMOVE STUDENT
        elif choice == "3":
            Student_id =input("Enter student ID: ")
            try :
                S = Student(dbb ,"" ,0,"",0,"")
                S.remove_stu(Student_id)
            except ValueError as e :
                print(e)    
        #>>>>>>.......................................DISPLAY STUDENTS TABLE
        elif choice == "4":
            query = "SELECT * FROM students"
            result = dbb.execute_query(query, fetch=True)
            if result:
                for row in result:
                    print(f"Student ID: {row[0]}, Name: {row[1]}, Grade: {row[2]}, Email: {row[3]}, Age: {row[4]}, Class ID: {row[5]}")
            else:
                print("No students Found !")
        #>>>>>>..........................................SEARCH
        elif choice == "5":
            student_id = input("Enter Student ID: ")
            S= Student(dbb,"",0,"",0)
            S.search_stu(student_id) 
        ####...................BACK
        elif choice == "6":
            break
        else:
            print("Invalid choice! Womp Womp !!!!!!!!")
            
  #>>>>>>>>>>>>>>..............>>>>>>>>>>>>>>>>>>>>   TEACHER MENU  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<         
def teacher_menu():
    while True:
        print("\n=====> Teacher Management <=====")
        print("\n1. Add a New Teacher")
        print("2. Update Teacher Details")
        print("3. Delete a Teacher")
        print("4. Show All Teachers")
        print("5. Search for a Teacher")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ")
        #>>>>>>..........................ADD TEACHER
        if choice == "1":
            name = input("Enter Teacher Name: ")
            email= input("Enter Teacher's Email: ")
            age =int(input("Enter teacher age:"))
            class_id =input("Enter teacher's Class ID: ")
            try :
                T = Teacher(dbb ,name , email ,age, class_id )
                T.add_t()
            except ValueError as e:
                print(e)
        #>>>....................................EDIT TEACHER            
        elif choice == "2":
            teacher_id = input("Enter Teacher ID: ")
            field = input("Enter The field To Update: ")
            value =input("Enter The new Value: ")
            try:   
                 T = Teacher(dbb , "", "", 0 , "")
                 T.edit_t(teacher_id , field, value)
            except ValueError as e: 
                print(e)
        ##>>>....................................REMOVE T
        elif choice == "3":
            teacher_id =input("Enter the Teacher ID: ")
            try:
                T=Teacher(dbb, "", "",0,"")
                T.remove_t(teacher_id)
            except ValueError as e :
                print(e)    
            
        ##>>....................................DISPLAYYYYY T
        elif choice == "4":
            query = "SELECT * FROM teachers"
            result = dbb.execute_query(query, fetch=True)
            if result:
                for row in result:
                    print(f"Teacher ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, age: {row[3]}, Class ID: {row[4]}, Course ID: {row[5]}")
            else:
                print("No Teachers Found ! !")
        ##>>.........................................SEARCH T
        elif choice == "5":
            teacher_id =input("Enter the Teacher ID: ")
            T=Teacher(dbb, "", "",0,"")
            T.search_t(teacher_id)
       ##>>....................................BACK TO MAIN     
        elif choice == "6":
            break
        else:
            print("Invalid choice! Please try again ! ! womp")
            
   #>>>>>>>>>.......>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  COURSE MENU  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<        
def course_menu():
    while True:
        print("\n=====> Course Management <=====")
        print("\n1. Add a New Course")
        print("2. Update Course Details")
        print("3. Delete a Course")
        print("4. Show All Courses")
        print("5. Search for a Course")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ")
        ###>>.....................................ADD COURSE
        if choice == "1":
            course_name = input("Enter name for the course: ")
            total_hours = input("Enter the course total hour: ")
            course_id = input("Enter an ID for the course: ")
            teacher_id = input("Enter The teacher ID for the course: ")
            class_id =input("Enter Class ID for the course: ")
            try:
               CC=Course(dbb, course_name ,total_hours,course_id, teacher_id, class_id )
               CC.add_course()
            except ValueError as e:
                print(e)   
               
        ###>>.................................EDIT COURSE                              
        elif choice == "2":
            course_id = input("Enter the Course ID to update: ")
            field = input("Enter the field(course_name, total_hours, teacher_id, class_id): ")
            value = input("Enter the new value: ")
            try:
                if field in ["total_hours"]:
                    value = int(value)  
                    
                CC = Course(dbb, "", 0, course_id, "", "")
                CC.edit_course(course_id, field, value)
                
            except ValueError as e:
                print(e)
        ##>>>......................................RENOVE COURSE
        elif choice == "3":
            course_id =input("Enter the course ID: ")
            try:
                CC=Course(dbb, "", 0, course_id, "", "")
                CC.remove_class(class_id)
                
            except ValueError as e:
                print(e)        
        ##>>.........................................DISPLAY
        elif choice == "4":
            query = "SELECT * FROM courses"
            result = dbb.execute_query(query, fetch=True)
            if result:
                print("\nAll Courses:")
                for row in result:
                    print(f"Course ID: {row[0]}, Name: {row[1]}, Total Hours: {row[2]}, Teacher ID: {row[3]}, Class ID: {row[4]}")
            else:
                print("No courses found!")
        ##>>.............................................SEARCH
        elif choice == "5":
            
            course_id=input("Enter Course ID: ")
            C = Course(dbb, "", 0, course_id, "", "")
            C.search_course(course_id)
        ##>>..............................................BACK
        elif choice == "6":
            break
        else:
            print("Invalid choice! use valid choices !!!!!")
            
   #>>>>>>>>>>>>>>>>>.......... REPORT MENU         
def report_menu():
    while True:
        print("\n=====> Reports and Visualization <=====")
        print("\n1. Display enrollment trends ")
        print("2. Analyze teacher workload")
        print("3. summarize student performance")
        print("4. Generate All Summary Report with CSV file")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ")
        ###..................................................
        if choice == "1":
           try:
              R=Reporting(dbb)
              R.display_enrollment_trends()
           except ValueError as e:
               print(e)
                  
        elif choice == "2":
            try:
              R=Reporting(dbb)
              R.analyze_teacher_workload()
            except ValueError as e :
                print(e)
                  
        elif choice == "3":
            try:
              R=Reporting(dbb)
              R.summarize_student_performance()
            except ValueError as e :
                 print(e)
                   
        ###.>>>>.........................generate all the Reports into CSV file........
        elif choice == "4":
            try:
              R=Reporting(dbb)
              R.class_summary_report()
              R.teacher_workload_report()
              R.student_performance_report()
              R.enrollment_trends_report()
              
            except ValueError as e :
                print(e)  
         ##...........................BACK
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
            

