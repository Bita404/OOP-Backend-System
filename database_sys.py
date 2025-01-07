import mysql.connector
import  pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
 ######................>>>> Student                      
class Student(person):
     Last_stuID = 1404000
     def __init__(self ,db, name , grade , email ,age ):
          super().__init__(name , email , age)
          self.db = db
          self.student_id = Student.StuID_gen()
          self.grade = grade
          self.class_id = None
          self.course_id = None

     @classmethod
     def StuID_gen(cls):
        Student_id = "S" + str(cls.Last_stuID)
        cls.Last_stuID += 1 
        return Student_id
        
     def add_stu (self):
          query = """
             INSERT INTO students (student_id, name, grade, email, age, class_id, course_id)
             VALUES (%s, %s, %s, %s, %s, %s, %s)
          """
          data = (self.student_id, self.name, self.grade, self.email, self.age, self.class_id, self.course_id)
          self.db.execute_query(query, data)
          
     def remove_stu (self, student_id):
         query = "DELETE FROM students WHERE student_id = %s"
         self.db.execute_query(query, (student_id,))
         print(f"Student {student_id} removed successfully.")
         
     def edit_stu (self, student_id, field, value):
          """ Updates a specific field of the student record """
          
          if field not in ["name", "grade", "email", "age", "class_id", "course_id"]:
               raise ValueError(f"Invalid field '{field}' provided for update.")
          
          query = f"UPDATE students SET {field} = %s WHERE student_id = %s"
          data = (value, student_id)
          self.db.execute_query(query, data)
          
     def search_stu (self , student_id):
          query = "SELECT * FROM students WHERE student_id = %s"
          return self.db.execute_query(query, (student_id,), fetch=True)
######................>>>>  teacher         
class Teacher (person):
     teacherID_list = {}
     Last_teacherID = 1000
     def __init__(self ,db ,name , email ,age ):
          super().__init__(name , email, age)
          self.db = db
          self.teacher_id = Teacher.TID_gen()
          self.course_id = None
          self.class_id = None
          Teacher.teacherID_list[self.teacher_id] = self
          
     @classmethod     
     def TID_gen(cls):
        teacher_id = "T" + str(cls.Last_teacherID)
        cls.Last_teacherID += 1 
        return teacher_id
          
     def add_t ():
          pass
     def remove_t ():
          pass
     def edit_t ():
          pass
     def search_t ():
          pass
 ######................>>>>  course    
class Course():
     course_list = {}
     def __init__(self, db , course_name , total_hours , course_id , teacher_id):  
          if course_id not in Course.course_list and teacher_id in Teacher.teacherID_list : 
              self.db = db 
              self.course_name = course_name
              self.total_hours = total_hours 
              self.course_id = course_id
              Course.course_list[course_id] = self
              self.teacher_id = teacher_id  
          else :
               raise ValueError("ID Error !!! This course ID might already exist OR Invalid teacher ID! ! ! ")
            
          
       
     def add_course ():
          pass
     def remove_course():
          pass
     def edit_course ():
          pass
     def search_course ():
          pass
     
######................>>>>  Class     
class Class :
     def __init__(self , class_id , class_name , student_id , teaacher_id ):
          pass
     def add_class ():
          pass
     def remove_class ():
          pass
     def edit_class ():
          pass
     def search_class ():
          pass
#........................................................................     
     
 
