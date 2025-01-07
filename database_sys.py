import mysql.connector
import  pandas as pd
import matplotlib.pyplot as plt
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
class DB_connection :
     def __init__(self, user, password, host, database , logger):
        self.user = user 
        self.password = password 
        self.host = host 
        self.databse = database
        self.connect = None
        self.logger = logger
        
     def connnection(self):
        self.connect = mysql.connector.connect(
          user = self.user,
          password = self.password,
          host = self.host,
          database = self.databse
        )   
        
     def execute_query(self, query, data=None, fetch=False):
        try:
            self.connnection() 
            mycursor = self.connect.cursor() 
            mycursor.execute(query, data)
        except Exception as e:
            print(e)
            self.logger.write_log("execute_query", f"Error: {e}")
        else:
            if fetch:
                data = mycursor.fetchall()
                self.logger.write_log("execute_query", "Query executed successfully with fetch")
                return data
            affected_rows = mycursor.rowcount
            self.connect.commit()
            self.logger.write_log("execute_query", f"Query executed successfully, {affected_rows} rows affected")
            return affected_rows
        finally:
            if self.connect.is_connected():
                mycursor.close()
                self.connect.close()  
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
     classID_list = {}
     def __init__(self ,db , class_id , class_name , class_capacity ):
          if class_id not in Class.classID_list : 
              if not isinstance(class_capacity, int) or class_capacity <= 0:
                 raise ValueError("Invalid class capacity! Must be a positive Number ! !")
              self.db = db 
              self.class_name = class_name 
              self.class_id = class_id
              self.class_capacity = class_capacity
              Class.classID_list[class_id] = self
          else :
               raise ValueError("ID Error !!! This class ID already exists ! ! ! ")
     
     def add_class (self):
          query = """
            INSERT INTO class (class_id, class_name , class_capacity)
            VALUES (%s, %s, %s)
          """
          data = (self.class_id, self.class_name, self.class_capacity)
          self.db.execute_query(query, data)
          
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
          return result
 ######................>>>> Student                      
class Student(person , Class):
     stu_list ={}
     Last_stuID = 1404000
     def __init__(self ,db, name , grade , email ,age, class_id ):
          super().__init__(name , email , age)
          Class.__init__(class_id)
          if class_id in Class.classID_list:
             self.db = db
             self.student_id = Student.StuID_gen()
             Student.stu_list[self.student_id] = self
             self.grade = grade
             self.class_id = class_id
          else :
               raise ValueError(f"'{self.class_id}' Invalid Class ID ! ! make the class first !")   

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
          
     def remove_stu (self, student_id):
         query = "DELETE FROM students WHERE student_id = %s"
         self.db.execute_query(query, (student_id,))
         print(f"Student {student_id} removed successfully.")
         
     def edit_stu (self, student_id, field, value):
          """ Updates a specific field of the student record """
          
          if field not in ["name", "grade", "email", "age", "class_id"]:
               raise ValueError(f"Invalid field '{field}' provided for update.")
          
          query = f"UPDATE students SET {field} = %s WHERE student_id = %s"
          data = (value, student_id)
          self.db.execute_query(query, data)
          
     def search_stu (self , student_id):
          query = "SELECT * FROM students WHERE student_id = %s"
          return self.db.execute_query(query, (student_id,), fetch=True)
     
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
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    def display_enrollment_trends(self):
        """Analyze course enrollment"""
        query = """
            SELECT courses.course_name, COUNT(students.student_id) AS enrollment_count, classes.class_name
            FROM students
            INNER JOIN classes ON students.class_id = classes.class_id
            INNER JOIN courses ON classes.class_id = courses.class_id
            GROUP BY courses.course_name, classes.class_name
        """
        data = self.db.execute_query(query, fetch=True)
        if not data:
            print("No enrollment data found!")
            return

        df = pd.DataFrame(data, columns=["Course Name", "Enrollment Count", "Class Name"])

        plt.figure(figsize=(10, 6))
        for course in df["Course Name"].unique():
            course_data = df[df["Course Name"] == course]
            plt.plot(course_data["Class Name"], course_data["Enrollment Count"], marker='o', label=course)

        plt.title("Enrollment Trends Over Time")
        plt.xlabel("Class Name")
        plt.ylabel("Enrollment Count")
        plt.legend()
        plt.grid()
        plt.show()

        self.logger.write_log("display_enrollment_trends", "Visualization generated successfully.")
        
   #>>>>>>>>>>>>>>>>>>> Teacher Report
    def analyze_teacher_workload(self):
        """Calculate and visualize teacher workload."""
        query = """
            SELECT teachers.name AS teacher_name, COUNT(courses.course_id) AS course_count, 
                   SUM((SELECT COUNT(student_id) FROM students WHERE students.class_id = courses.class_id)) AS total_students
            FROM teachers
            LEFT JOIN courses ON teachers.teacher_id = courses.teacher_id
            GROUP BY teachers.name
        """
        data = self.db.execute_query(query, fetch=True)
        if not data:
            print("No teacher workload data found!")
            return

        df = pd.DataFrame(data, columns=["Teacher Name", "Course Count", "Total Students"])

        df.plot(x="Teacher Name", y=["Course Count", "Total Students"], kind="bar", figsize=(10, 6))
        plt.title("Teacher Workload Analysis")
        plt.xlabel("Teacher Name")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.legend(["Courses", "Students"])
        plt.grid(axis="y")
        plt.show()

        self.logger.write_log("analyze_teacher_workload", "Visualization generated successfully.")
        
  #>>>>>>>>>>>>>>>>>>>>>>>> student report
    def summarize_student_performance(self, student_id):
        """Visualize a student's performance across courses."""
        query = """
            SELECT courses.course_name, students.grade
            FROM students
            INNER JOIN courses ON students.class_id = courses.class_id
            WHERE students.student_id = %s
        """
        data = self.db.execute_query(query, (student_id,), fetch=True)
        if not data:
            print(f"No performance data found for Student ID: {student_id}")
            return

        df = pd.DataFrame(data, columns=["Course Name", "Grade"])

        plt.figure(figsize=(10, 6))
        plt.plot(df["Course Name"], df["Grade"], marker='o', linestyle='-', color='b', label="Grade")
        plt.title(f"Student Performance Overview (Student ID: {student_id})")
        plt.xlabel("Course Name")
        plt.ylabel("Grade")
        plt.ylim(0, 100)
        plt.grid()
        plt.legend()
        plt.show()

        self.logger.write_log("summarize_student_performance", f"Performance visualization generated for Student ID: {student_id}.")
    
 
