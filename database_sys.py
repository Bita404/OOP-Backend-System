import mysql.connector
import  pandas as pd
import matplotlib.pyplot as plt

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