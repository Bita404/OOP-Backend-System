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
########>>>>>>>>>>>>>>> base class for any person in the system               
class person :
     def __init__(self , name, email , age):
          self.name = name
          self.email = email
          self.age = age  
          
     def __str__(self):
          return f"person name:{self.name}, {self.age} years old, with email: {self.email}"  
     
 #.................................................................................................                      
 ######................>>>>  CLASS (base class for teacher and student)    
class Class :
     #classID_list = {} its already in the database 
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
          #Class.classID_list[self.class_id] = self
          
     def remove_class(self , class_id):
          query = "DELETE FROM classes WHERE class_id = %s"
          data = (class_id,)
          self.db.execute_query(query, data)
          
     def edit_class(self, class_id, field, value):
          if field not in ["class_name", "class_capacity"]:
            raise ValueError(f"Invalid field '{field}' provided for update.")

          query = f"UPDATE classes SET {field} = %s WHERE class_id = %s"
          data = (value, class_id)
          self.db.execute_query(query, data)
          
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
 ######................>>>> Student                      
class Student(person , Class):
     stu_list ={}
     Last_stuID = 1404000
     
     def __init__(self ,db, name , grade , email ,age, class_id ):
          super().__init__(name , email , age)
          Class.__init__(class_id)
          if not isinstance(age, int) or not isinstance(grade, int) or grade>100 or grade<0 or age<5 or age>18 :
                 raise ValueError("Invalid Age or grade Number ! !  ")
          self.db = db
          self.student_id = Student.StuID_gen()
          Student.stu_list[self.student_id] = self
          self.grade = grade
          self.class_id = class_id 

     @classmethod
     def StuID_gen(cls):
        Student_id = "S" + str(cls.Last_stuID)
        cls.Last_stuID += 1 
        return Student_id
        
     def add_stu (self):
          query = """
             INSERT INTO students (student_id, name, grade, email, age, class_id)
             VALUES (%s, %s, %s, %s, %s, %s)
          """
          data = (self.student_id, self.name, self.grade, self.email, self.age, self.class_id)
          self.db.execute_query(query, data)
          print(f"Student added successfully! Assigned Student ID: {self.student_id}")
          
     def remove_stu (self, student_id):
         if not self.is_student_id_valid(student_id):
            print(f"Student ID '{student_id}' does not exist.")
            return
         query = "DELETE FROM students WHERE student_id = %s"
         self.db.execute_query(query, (student_id,))
         print(f"Student {student_id} removed successfully.")
         
     def edit_stu (self, student_id, field, value):
          """ Updates a specific field of the student record """
          if not self.is_student_id_valid(student_id):
            print(f"Student ID '{student_id}' does not exist.")
            return
        
          if field not in ["name", "grade", "email", "age", "class_id"]:
               raise ValueError(f"Invalid field '{field}' provided for update.")
          
          query = f"UPDATE students SET {field} = %s WHERE student_id = %s"
          data = (value, student_id)
          self.db.execute_query(query, data)
          
     def search_stu (self , student_id):
          query = "SELECT * FROM students WHERE student_id = %s"
          result =  self.db.execute_query(query, (student_id,), fetch=True)
          if result:
            print("Student found:")
            for row in result:
                print(f"Student ID: {row[0]}, Name: {row[1]}, Grade: {row[2]}, Email: {row[3]}, Age: {row[4]}, Class ID: {row[5]}")
            return result
          else:
            print(f"Student ID '{student_id}' Not Found ! ")
            return None
        #>>>>>>>>>>>>>>> Check in database to see if id is valid or not <<<<<<<
     def is_student_id_valid(self, student_id):
        query = "SELECT COUNT(*) FROM students WHERE student_id = %s"
        result = self.db.execute_query(query, (student_id,), fetch=True)
        return result[0][0] > 0 
     
######................>>>>  teacher         
class Teacher (person, Class):
     teacherID_list = {}
     Last_teacherID = 1000
     def __init__(self ,db ,name , email ,age, class_id ):
          super().__init__(name , email, age)
          Class.__init__(class_id)
          if class_id in Class.classID_list :
             self.db = db
             self.teacher_id = Teacher.TID_gen()
             self.course_id = None
             self.class_id = class_id
             Teacher.teacherID_list[self.teacher_id] = self
          else :
             raise ValueError(f"'{self.class_id}' Invalid Class ID ! ! make the class first !")   
          
     @classmethod     
     def TID_gen(cls):
        teacher_id = "T" + str(cls.Last_teacherID)
        cls.Last_teacherID += 1 
        return teacher_id
          
     def add_t(self):
          query = """
            INSERT INTO teachers (teacher_id, name, email, age, class_id, course_id)
            VALUES (%s, %s, %s, %s, %s, %s)
          """
          data = (self.teacher_id, self.name, self.email, self.age, self.class_id, self.course_id)
          self.db.execute_query(query, data)
          
     def remove_t(self, teacher_id):
          query = "DELETE FROM teachers WHERE teacher_id = %s"
          self.db.execute_query(query, (teacher_id,))
          print(f"Teacher {teacher_id} removed successfully.")
          
     def edit_t(self,teacher_id , field , value):
          """Updates a specific field of the teacher record"""
          valid_fields = ["name", "email", "age", "course_id", "class_id"]
        
          if field not in valid_fields:
               raise ValueError(f"Invalid field '{field}' provided for update.")
        
          query = f"UPDATE teachers SET {field} = %s WHERE teacher_id = %s"
          data = (value, teacher_id)
          self.db.execute_query(query, data)
          
     def search_t(self, teacher_id):
          query = "SELECT * FROM teachers WHERE teacher_id = %s"
          data = (teacher_id,)
          return self.db.execute_query(query, data, fetch=True)
 ######................>>>>  course    
class Course(Class):
     course_list = {}
     def __init__(self, db , course_name , total_hours , course_id , teacher_id, class_id):  
          Class.__init__(class_id)
          if course_id not in Course.course_list:
               if teacher_id in Teacher.teacherID_list:
                   if class_id in Class.classID_list: 
                       self.db = db 
                       self.course_name = course_name
                       self.total_hours = total_hours 
                       self.course_id = course_id
                       Course.course_list[course_id] = self
                       self,class_id = class_id
                       self.teacher_id = teacher_id  
                   else:
                        raise ValueError("ID Error ! ! Invalid Class ID !")  
               else :
                    raise ValueError("ID Error! Invaild Teacher ID ! ")     
                         
          else :
               raise ValueError("ID Error!!! This Course ID already Exists ! ! !")
            
     def add_course(self):
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
          self.db.logger.write_log("add_course", f"Course {self.course_id} added successfully and teacher {self.teacher_id} updated with course_id.")
          
     def remove_course(self, course_id):
          query = "DELETE FROM courses WHERE course_id = %s"
          data = (course_id,)
          self.db.execute_query(query, data)
          
     def edit_course (self, course_id, field, value):
          if field not in ["course_name", "total_hours", "teacher_id", "class_id"]:
             raise ValueError(f"Invalid field '{field}' provided for update.")

          query = f"UPDATE courses SET {field} = %s WHERE course_id = %s"
          data = (value, course_id)
          self.db.execute_query(query, data)
          
     def search_course (self, course_id):
          query = "SELECT * FROM courses WHERE course_id = %s"
          data = (course_id,)
          result = self.db.execute_query(query, data, fetch=True)
          return result
#........................................................................     
#####>>>>>>>>>>>>>>>>>>>> Visualization and Reports 
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
            print(f"Class summary report saved to {filename}.")
        else:
            print("No data found for class summary report.")

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
            print("No data found for enrollment trends report.")

    # ----------------- Data Visualization -----------------
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
            print("No data available to display enrollment trends.")

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
            print("No data available to analyze teacher workload.")

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
            print(f"No performance data available for student ID {student_id}.")
            
            
logger = Logger()

dbb = DB_connection("root", "Bita1380", "localhost", "school_sys", logger)

query = "SELECT * FROM classes"
result = dbb.execute_query(query, fetch=True)
if result:
    for row in result:
        print(row)
