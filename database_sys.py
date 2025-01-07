import mysql.connector
import  pandas as pd
import matplotlib.pyplot as plt
import logging
from datetime import datetime

#############>>>>>>> database connection  <<<<<<<<<<#########
class DB_connection :
     def __init__(self, user, password, host, database):
        self.user = user 
        self.password = password 
        self.host = host 
        self.databse = database
        self.connect = None
        
     def connnection(self):
        self.connect = mysql.connector.connect(
          user = self.user,
          password = self.password,
          host = self.host,
          database = self.databse
        )   
        
     def execute_query(self, query, data=None, 
                      fetch=False):
        try:
            self.connnection() 
            mycursor = self.connect.cursor() 
            mycursor.execute(query, data)
        except Exception as e:
            print(e)
        else:
            if fetch:
                data = mycursor.fetchall()
                return data
            affected_rows = mycursor.rowcount
            self.connect.commit()
            return affected_rows
        finally:
            if self.connect.is_connected():
                mycursor.close()
                self.connect.close()  
                
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
          pass
     def remove_stu (self):
          pass
     def edit_stu ():
          pass
     def search_stu ():
          pass
######................>>>>  teacher         
class Teacher (person):
     Last_teacherID = 1000
     def __init__(self ,db ,name , email ,age ):
          super().__init__(name , email, age)
          self.db = db
          self.teacher_id = Teacher.TID_gen()
          self.course_id = None
          self.class_id = None
          
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
     def __init__(self, db , ):   
         
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
     def __init__(self , class_id , class_number ):
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
####################>>>>>>> LOG INFO FILE     
class log:
     def __init__(self):
          pass     
