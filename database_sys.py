import mysql.connector
import  pandas as pd
import matplotlib.pyplot as plt
import logging

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
                 
class DB:
    def __init__(self, db):
        self.db = db
                        
class Student (DB):
     def __init__(self ,db, student_id ,name , email , class_id):
          super().__init__(db)
          self.student_id = student_id
          self.name = name
          self.email = email
          self.class_id = class_id

          
     def add_stu (self):
          pass
     def remove_stu (self):
          pass
     def edit_stu ():
          pass
     def search_stu ():
          pass
          
class Teacher :
     def __init__(self):
         pass
     def add_t ():
          pass
     def remove_t ():
          pass
     def edit_t ():
          pass
     def search_t ():
          pass
    
class Course : 
     def __init__(self):
         pass
     def add_course ():
          pass
     def remove_course():
          pass
     def edit_course ():
          pass
     def search_course ():
          pass
class Class :
     def __init__(self):
          pass
     def add_class ():
          pass
     def remove_class ():
          pass
     def edit_class ():
          pass
     def search_class ():
          pass
     
class logger:
     def __init__(self):
          pass     
                  