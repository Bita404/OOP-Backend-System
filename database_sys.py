import mysql.connector
import  pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
#################################
# user input oder : 
# 1.classes   2.person(students , teachers)  3.courses
#since every oject in this project shares some same attributes and requiers user to input valid ones 
####################>>>>>>> LOG INFO FILE
class Logger:
    def __init__(self, log_file="System.log"):
        """ System Log maker """
        self.log_file = log_file

    def write_log(self, cmd, outcome):
        with open(self.log_file, "a") as file:
            time_now = datetime.now().strftime("%d/%m/%Y--%I:%M-%p")
            text = f"{cmd}: {time_now} | Outcome: {outcome}\n"
            file.write(text)
            
#############>>>>>>> database connection  <<<<<<<<<<#########
import mysql.connector

class DB_connection:
    def __init__(self, user, password, host, database, logger):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection = None
        self.logger = logger

    def connect(self):
        """connect to the database"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    database=self.database
                )
                self.logger.write_log("connect", "Database connection established")
        except mysql.connector.Error as e:
            self.logger.write_log("connect", f"Connection error: {e}")
            print(f"Connection error: {e}")
            self.connection = None
    #>...........execute QUERY and FETCH RESULT
    def execute_query(self, query, data=None, fetch=False):
        """ Execute query """
        try:
            self.connect()  
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            if fetch:
                result = cursor.fetchall()
                self.logger.write_log("execute_query", "Query executed with fetch")
                return result
            self.connection.commit()
            self.logger.write_log("execute_query", "Query executed successfully")
        except mysql.connector.Error as e:
            self.logger.write_log("execute_query", f"Error executing query: {e}")
            print(f"Error executing query: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()  

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.write_log("close", "Database connection closed")
#.........................................................................................................               
########>>>>>>>>>>>>>>> base class for any PERSON in the system <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<               
class person :
     def __init__(self , name, email , age):
          self.name = name
          self.email = email
          self.age = age  
          
     def __str__(self):
          return f"person name:{self.name}, {self.age} years old, with email: {self.email}"  
     
 #.................................................................................................                      
 ######................>>>>  CLASS CLASS (base class for teacher and student) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   
class Class :
     #classID_list ={}
     def __init__(self ,db , class_id , class_name , class_capacity ):
          
              if not isinstance(class_capacity, int) or class_capacity < 0:
                 raise ValueError("Invalid class capacity! Must be a positive Number ! !")
              self.db = db 
              self.class_name = class_name 
              self.class_id = class_id
              self.class_capacity = class_capacity
     
     def add_class (self):
          query = """
            INSERT INTO classes (class_id, class_name , class_capacity)
            VALUES (%s, %s, %s)
          """
          data = (self.class_id, self.class_name, self.class_capacity)
          self.db.execute_query(query, data)
          print(f"\nClass '{self.class_name}' Added successfully, ID: {self.class_id}")
       #...........................................REMOVE CLASS.................................   
     def remove_class(self , class_id):
         
          if not self.is_class_id_valid(class_id):
            print(f"Class ID '{class_id}' does not exist.")
            return
          query = "DELETE FROM classes WHERE class_id = %s"
          data = (class_id,)
          self.db.execute_query(query, data)
          print(f"\nClass ID :'{class_id}' Removed Successfully !")
       #...............................................EDIT CLASS..........................   
     def edit_class(self, class_id, field, value):
         
          if not self.is_class_id_valid(class_id):
            print(f"\nClass ID '{class_id}' does Not exist !")
            return
        
          if field not in ["class_name", "class_capacity"]:
            raise ValueError(f"Invalid field '{field}' provided for update !")

          query = f"UPDATE classes SET {field} = %s WHERE class_id = %s"
          data = (value, class_id)
          self.db.execute_query(query, data)
          print(f"\nClass :'{class_id}' Updated !")
          
       #.............................................SEARCH CLASS.......................   
     def search_class(self , class_id):
          query = "SELECT * FROM classes WHERE class_id = %s"
          data = (class_id,)
          result = self.db.execute_query(query, data, fetch=True)
          if result:
               for row in result:
                   print(f"\n Class ID: {row[0]}, Name: {row[1]}, Capacity: {row[2]}")
                   return result
          else:
                print(f"\n No class found with ID: {self.class_id}")
                return None
       #.......................................VALIDATE CLASS......................
     def is_class_id_valid(self, class_id):   #########Check the classes table to see if ID is valid or no 
         
        query = "SELECT COUNT(*) FROM classes WHERE class_id = %s"
        result = self.db.execute_query(query, (class_id,), fetch=True)
        return result[0][0] > 0       
    
 ######................>>>>>>>>>>>>>>>>>>>>>>> Student <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                      
class Student(person , Class):
     #stu_list ={}
     #Last_stuID = 1404000
     
     def __init__(self ,db, name , grade , email ,age, student_id, class_id ):
          super().__init__(name , email , age)
          Class.__init__(self ,db, class_id,"",0)
          
          if not isinstance(age, int) or not isinstance(grade, int) or grade>100 or grade<0 or age<5 or age>30 :
                 raise ValueError("Invalid Age or grade Number ! !  ")
             
          self.db = db
          self.student_id =  student_id #Student.StuID_gen() useless method
          self.grade = grade
          self.age =age
          self.email = email
          self.class_id = class_id 

    # @classmethod       >>>>>>>>>>>>>>>>>> this method resets after ending the program 
     #def StuID_gen(cls):                       not a good idea for SQL DB primery keys
      #  Student_id = "S" + str(cls.Last_stuID)
       # cls.Last_stuID += 1 
        #return Student_id
        
     def add_stu (self):
         
          if not self.is_class_id_valid(self.class_id):
              raise ValueError(f"ID Error: Invalid Class ID '{self.class_id}'!")
          
          query = """
             INSERT INTO students (student_id, name, grade, email, age, class_id)
             VALUES (%s, %s, %s, %s, %s, %s)
          """
          data = (self.student_id, self.name, self.grade, self.email, self.age, self.class_id)
          self.db.execute_query(query, data)
          print(f"\nStudent Added successfully! Student ID: {self.student_id}")
     ###.....................................................................     
     def remove_stu (self, student_id):
         if not self.is_student_id_valid(student_id):
            print(f"Student ID '{student_id}' INVALID !")
            return
         query = "DELETE FROM students WHERE student_id = %s"
         self.db.execute_query(query, (student_id,))
         print(f"\nStudent {student_id} Removed !")
     #........................................................................    
     def edit_stu (self, student_id, field, value):
          """ Update """
          if not self.is_student_id_valid(student_id):
            print(f"\nStudent ID '{student_id}' does Not exist !")
            return
        
          if field not in ["name", "grade", "email", "age", "class_id"]:
               raise ValueError(f"Invalid field '{field}' provided for update.")
          
          query = f"UPDATE students SET {field} = %s WHERE student_id = %s"
          data = (value, student_id)
          self.db.execute_query(query, data)
          print("\nStudent Updated")
       #........................................................................................   
     def search_stu (self , student_id):
          query = "SELECT * FROM students WHERE student_id = %s"
          result =  self.db.execute_query(query, (student_id,), fetch=True)
          if result:
            print("\nStudent found:")
            for row in result:
                print(f"Student ID: {row[0]}, Name: {row[1]}, Grade: {row[2]}, Email: {row[3]}, Age: {row[4]}, Class ID: {row[5]}")
            return result
          else:
            print(f"\nStudent ID '{student_id}' Not Found ! ")
            return None
        #>>>>>>>>>>>>>>> Check in database to see if id is valid or not <<<<<<<
     def is_student_id_valid(self, student_id):
        query = "SELECT COUNT(*) FROM students WHERE student_id = %s"
        result = self.db.execute_query(query, (student_id,), fetch=True)
        return result[0][0] > 0 
    
     def is_class_id_valid(self, class_id):
        query = "SELECT COUNT(*) FROM classes WHERE class_id = %s"
        result = self.db.execute_query(query, (class_id,), fetch=True)
        return result[0][0] > 0
     
######.............>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.>>>>  TEACHER CLASS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<        
class Teacher (person, Class):
     #teacherID_list = {}
     #Last_teacherID = 1000
     def __init__(self ,db ,name , email ,age, teacher_id ,class_id ):
          super().__init__(name , email, age)
          Class.__init__(self ,db, class_id,"",0)
          
          self.db = db
          self.teacher_id =  teacher_id  #Teacher.TID_gen() >>> useless method
          self.course_id = None
          self.class_id = class_id
          #Teacher.teacherID_list[self.teacher_id] = self
  
     #@classmethod     ##### if u run the code more than once this ID generator resets T T 
     #def TID_gen(cls):
      #  teacher_id = "T" + str(cls.Last_teacherID)
       # cls.Last_teacherID += 1 
        #return teacher_id
       #.....................................................................   
     def add_t(self):
          if not self.is_class_id_valid(self.class_id):
              raise ValueError(f"ID Error: Invalid Class ID '{self.class_id}'!")
          
          if not isinstance(self.age, int) or  self.age<20 or self.age>60 :
                 raise ValueError("Invalid age! teacher age must be between 20 to 60 ! ! ") 
             
          query = """
            INSERT INTO teachers (teacher_id, name, email, age, class_id, course_id)
            VALUES (%s, %s, %s, %s, %s, %s)
          """
          data = (self.teacher_id, self.name, self.email, self.age, self.class_id, self.course_id)
          self.db.execute_query(query, data)
          print(f"Teacher Added Successfully! ")
    ###.......................................REMOVE...........TEACHERRRR.............................   
     def remove_t(self, teacher_id):
          if not self.is_TEACHER_valid(teacher_id):
              print(f"INVALID ID '{teacher_id}' !")
              return
          query = "DELETE FROM teachers WHERE teacher_id = %s"
          self.db.execute_query(query, (teacher_id,))
          print(f"Teacher {teacher_id} Removed !")
     ##.............................................EDIT TEACHERRRRRRR...............................     
     def edit_t(self,teacher_id , field , value):
         
          if not self.is_TEACHER_valid(teacher_id):
              print(f"INVALID ID '{teacher_id}' !")
              return
          valid_fields = ["name", "email", "age", "course_id", "class_id"]
        
          if field not in valid_fields:
               raise ValueError(f"Invalid field '{field}' provided for update.")
        
          query = f"UPDATE teachers SET {field} = %s WHERE teacher_id = %s"
          data = (value, teacher_id)
          self.db.execute_query(query, data)
          print("\nTeacher Updated")
       ##.........................................SEARCHHHHHH................................   
     def search_t(self, teacher_id):
          query = "SELECT * FROM teachers WHERE teacher_id = %s"
          data = (teacher_id,)
          result = self.db.execute_query(query, data, fetch=True)
          if result:
            print("\nTeacher Found:")
            for row in result:
                print(f"Teacher ID: {row[0]}, Name: {row[1]}, email: {row[2]}, age: {row[3]},Class ID: {row[4]},Course ID:{row[5]}")
            return result
          else:
            print(f"\nTeacher ID '{teacher_id}' Not Found ! ")
            return None
      #.............................................VALIDATE TEACHERRRR.........................
     def is_TEACHER_valid(self, teacher_id):
        query = "SELECT COUNT(*) FROM teachers WHERE teacher_id = %s"
        result = self.db.execute_query(query, (teacher_id,), fetch=True)
        return result[0][0] > 0 
    
     def is_class_id_valid(self, class_id):
        query = "SELECT COUNT(*) FROM classes WHERE class_id = %s"
        result = self.db.execute_query(query, (class_id,), fetch=True)
        return result[0][0] > 0  
    
 ######.......>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> COURSE CLASS  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
class Course(Class):
     course_list = {}
     def __init__(self, db , course_name , total_hours , course_id , teacher_id, class_id):  
          Class.__init__(self ,db, class_id,"",0)
          self.db = db 
          self.course_name = course_name
          self.total_hours = total_hours 
          self.course_id = course_id
          #Course.course_list[course_id] = self
          self.class_id = class_id
          self.teacher_id = teacher_id  
          
     def add_course(self):
         
          if self.is_course_id_valid(self.course_id):
             raise ValueError(f"ID Error: Course ID '{self.course_id}' already exists!")

          elif not self.is_Teacher_valid(self.teacher_id):
              raise ValueError(f"ID Error: Invalid Teacher ID '{self.teacher_id}'!")

          elif not self.is_class_id_valid(self.class_id):
              raise ValueError(f"ID Error: Invalid Class ID '{self.class_id}'!")
          #####............. totar must be number and +
          elif not isinstance(self.total_hours, int) or self.total_hours <= 0:
            raise ValueError("Invalid total hours! It must be a positive integer!!!!")
        
          else: 
           query = """
             INSERT INTO courses (course_id, course_name, total_hours, teacher_id ,class_id)
             VALUES (%s, %s, %s, %s, %s)
           """
           data = (self.course_id, self.course_name, self.total_hours, self.teacher_id, self.class_id)
           self.db.execute_query(query, data)
          
          #>>>>>> need to add the new course to teacher aswell
           update_query = "UPDATE teachers SET course_id = %s WHERE teacher_id = %s"
           update_data = (self.course_id, self.teacher_id)
           self.db.execute_query(update_query, update_data)
          
           print(f"\nCourse '{self.course_name}' (ID: {self.course_id}) added successfully!")
      #....................................................ADD......................    
     def remove_course(self, course_id):
         
          if not self.is_course_id_valid(course_id):
            print(f"\nID Error: Course ID '{course_id}' does Not exist !!!!")
            return
          query = "DELETE FROM courses WHERE course_id = %s"
          data = (course_id,)
          self.db.execute_query(query, data)
          print(f"\nCourse ID '{course_id}' removed successfully.")
      #....................................................EDIT...............    
     def edit_course (self, course_id, field, value):
         
          if not self.is_course_id_valid(course_id):
            print(f"ID Error: Course ID '{course_id}' does Not exist ! !")
            return
          if field not in ["course_name", "total_hours", "teacher_id", "class_id"]:
             raise ValueError(f"Invalid field '{field}' ! ")
         
          if field == "total_hours":
            if not isinstance(value, int) or value <= 0:
                raise ValueError("Invalid total hours! It must be a positive integer.")
          elif field == "teacher_id" and not self.is_teacher_id_valid(value):
                raise ValueError(f"Invalid Teacher ID '{value}'!")
          elif field == "class_id" and not self.is_class_id_valid(value):
                raise ValueError(f"Invalid Class ID '{value}'!")

          query = f"UPDATE courses SET {field} = %s WHERE course_id = %s"
          data = (value, course_id)
          self.db.execute_query(query, data)
          print(f"\nCourse ID '{course_id}' updated successfully !!!")
      #..............................................SEARCH...................    
     def search_course (self, course_id):
          query = "SELECT * FROM courses WHERE course_id = %s"
          data = (course_id,)
          result = self.db.execute_query(query, data, fetch=True)
          
          if result:
            print("\nCourse Found:")
            for row in result:
                print(f"Course ID: {row[0]}, Name: {row[1]}, Total Hours: {row[2]}, Teacher ID: {row[3]}, Class ID: {row[4]}")
            return result
          else:
            print(f"\ncourse: {course_id} Not Found ! ")
            return None
      #.............................................validate
     def is_course_id_valid(self, course_id):
        query = "SELECT COUNT(*) FROM courses WHERE course_id = %s"
        result = self.db.execute_query(query, (course_id,), fetch=True)
        return result[0][0] > 0

     def is_Teacher_valid(self, teacher_id):
        query = "SELECT COUNT(*) FROM teachers WHERE teacher_id = %s"
        result = self.db.execute_query(query, (teacher_id,), fetch=True)
        return result[0][0] > 0
    
     def is_class_id_valid(self, class_id):
        query = "SELECT COUNT(*) FROM classes WHERE class_id = %s"
        result = self.db.execute_query(query, (class_id,), fetch=True)
        return result[0][0] > 0  
#........................................................................     
#####>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Visualization and Reports <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class Reporting:
    def __init__(self, db):
        self.db = db

    def execute_query(self, query, params=None):
        """ to execute database queries """
        try:
            return self.db.execute_query(query, params, fetch=True)
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    # -------------------- CSV Reports --------------------
    def class_summary_report(self, filename="class_summary.csv"):
        query = """
            SELECT class_id, class_name, class_capacity 
            FROM classes
        """
        data = self.execute_query(query)
        if data:
            df = pd.DataFrame(data, columns=["Class ID", "Class Name", "Class Capacity"])
            df.to_csv(filename, index=False)
            print(f"\nClass summary report saved to {filename}.")
        else:
            print("\nNo data found for class summary report !!! ")

    def teacher_workload_report(self, filename="teacher_workload.csv"):
        query = """
            SELECT teachers.teacher_id, teachers.name, COUNT(DISTINCT courses.course_id) AS total_courses, 
                   COUNT(DISTINCT students.student_id) AS total_students
            FROM teachers
            LEFT JOIN courses ON teachers.teacher_id = courses.teacher_id
            LEFT JOIN students ON courses.class_id = students.class_id
            GROUP BY teachers.teacher_id, teachers.name
        """
        data = self.execute_query(query)
        if data:
            df = pd.DataFrame(data, columns=["Teacher ID", "Teacher Name", "Total Courses", "Total Students"])
            df.to_csv(filename, index=False)
            print(f"Teacher workload report saved to {filename}.")
        else:
            print("No data found for teacher workload report.")

    def student_performance_report(self, filename="student_performance.csv"):
        query = """
            SELECT students.student_id, students.name, courses.course_name, students.grade
            FROM students
            LEFT JOIN courses ON students.class_id = courses.class_id
        """
        data = self.execute_query(query)
        if data:
            df = pd.DataFrame(data, columns=["Student ID", "Student Name", "Course Name", "Grade"])
            df.to_csv(filename, index=False)
            print(f"Student performance report saved to {filename}.")
        else:
            print("No data found for student performance report.")

    def enrollment_trends_report(self, filename="enrollment_trends.csv"):
        query = """
            SELECT class_id, COUNT(student_id) AS total_students, YEAR(created_at) AS year
            FROM students
            GROUP BY class_id, YEAR(created_at)
            ORDER BY year
        """
        data = self.execute_query(query)
        if data:
            df = pd.DataFrame(data, columns=["Class ID", "Total Students", "Year"])
            df.to_csv(filename, index=False)
            print(f"Enrollment trends report saved to {filename}.")
        else:
            print("No data found for enrollment trends report !! ")

    # ------>>>>>>>>>>>>>>----------- Data Visualization --------<<<<<<<<<<<<<<<<---------
    def display_enrollment_trends(self):
        query = """
            SELECT YEAR(created_at) AS year, COUNT(student_id) AS total_students
            FROM students
            GROUP BY year
            ORDER BY year
        """
        data = self.execute_query(query)
        if data:
            df = pd.DataFrame(data, columns=["Year", "Total Students"])
            plt.figure(figsize=(10, 6))
            plt.plot(df["Year"], df["Total Students"], marker="o", linestyle="-", color="b")
            plt.title("Enrollment Trends Over Time")
            plt.xlabel("Year")
            plt.ylabel("Total Students")
            plt.grid(True)
            plt.show()
        else:
            print("\nNo data available to display enrollment trends ! ! ")

    def analyze_teacher_workload(self):
        query = """
            SELECT teachers.name, COUNT(DISTINCT courses.course_id) AS total_courses, 
                   COUNT(DISTINCT students.student_id) AS total_students
            FROM teachers
            LEFT JOIN courses ON teachers.teacher_id = courses.teacher_id
            LEFT JOIN students ON courses.class_id = students.class_id
            GROUP BY teachers.name
        """
        data = self.execute_query(query)
        if data:
            df = pd.DataFrame(data, columns=["Teacher Name", "Total Courses", "Total Students"])

            x = np.arange(len(df["Teacher Name"]))
            width = 0.35

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(x - width / 2, df["Total Courses"], width, label="Courses")
            ax.bar(x + width / 2, df["Total Students"], width, label="Students")

            ax.set_xlabel("Teachers")
            ax.set_ylabel("Count")
            ax.set_title("Teacher Workload Analysis")
            ax.set_xticks(x)
            ax.set_xticklabels(df["Teacher Name"], rotation=45, ha="right")
            ax.legend()

            plt.tight_layout()
            plt.show()
        else:
            print("\nNo data available to analyze teacher workload ! ! ")

    def summarize_student_performance(self, student_id):
        query = """
            SELECT courses.course_name, students.grade
            FROM students
            INNER JOIN courses ON students.class_id = courses.class_id
            WHERE students.student_id = %s
        """
        data = self.execute_query(query, (student_id,))
        if data:
            df = pd.DataFrame(data, columns=["Course Name", "Grade"])

            plt.figure(figsize=(10, 6))
            plt.plot(df["Course Name"], df["Grade"], marker="o", linestyle="-", color="g")
            plt.title(f"Performance Overview for Student {student_id}")
            plt.xlabel("Course")
            plt.ylabel("Grade")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
        else:
            print(f"\nNo data for student ID {student_id} !")
            
            
logger = Logger()

dbb = DB_connection("root", "Bita1380", "localhost", "school_sys", logger)

query = "SELECT * FROM classes"
result = dbb.execute_query(query, fetch=True)
if result:
    for row in result:
        print(row)
