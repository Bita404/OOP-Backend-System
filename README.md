# :pencil2: Backend System for managing school operations :pencil2:
This project is an OOP based backend system for managing school operations like teachers , students , classes and courses.
It contains all the CRUD operations for each object in the school and also contains visualization, analyzing and summery Reports to help the user.
Errors  in this project is handled .
## Libraries :books:
- mysql.connector
- pandas 
- matplotlib.pyplot
- numpy
- datetime
- MongoClient from pymongo
- database_sys ( this is my own program which I imported in main.py)
## database_sys.py :sunflower:
This is the main progaram , an OOP based Python code that provides:
- a class fro connecting to database
- a base person class that is going to be used as inheritance for Teacher class and Student Class since every person should have name, age and email 
- Class Class for managing Class ID , class capacity and Class name
- Class Students
- Class Teacher
- Class Course 
- Class Reporting : this class contains 2 parts part1 for CSV Reports and part2 for vizualization
### any of Class,Student,Teacher and Course classes contain All the CRUD opertaion(Add,Remove,Update,Display and Search) Functions in their Class and they also got defs for checking validations of each users ID befor running the CRUD opperations to avoid mistakes
## SQL Database (schoool_sys.sql)
this was coded in mysql command line to make the database and its table there fisrt and all the school datas in python code inserted there
## main.py :cherry_blossom:
This file contains the main menu code. The manu is made for easier use of the program (database_sys.py)
- Main menu: provides 7 options and the first 5 options has their own menu with other diffrent options.
- the menu has atleast more than 35 Options for all the operations
- Avdanced Search : helps to search with filter by anything
  ## Reporting class :chart_with_upwards_trend:
  data anlysis and visualizaion for school operation  
## CSV files :file_folder:
in the Reporting Class made an option for generationg summery reports from each table in the database 
## :leaves: with mongodb :leaves:
this program has same functionality like the database_sys.py but made with mongoDB 
## System.log
- Logging System Activities
## tables.txt 
the actual tables for this backend system
mysql> show tables;
- +----------------------+
- | Tables_in_school_sys |
- +----------------------+
- | classes              |
- | courses              |
- | students             |
- | teachers             |
- +----------------------+
