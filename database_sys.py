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
                
class                 
                