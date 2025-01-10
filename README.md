# :pencil2: Backend System for managing school operations :pencil2:
This project is an OOP based backend system for managing school operations like teachers , students , classes and courses.
It contains visualization and summery Reports to help.
## Libraries 
- mysql.connector
- pandas 
- matplotlib.pyplot
- numpy
- datetime
- MongoClient from pymongo
- database_sys ( this is my own program which I imported in main.py)
## database_sys.py 
This is the main progaram , an OOP based Python code that provides:
- a class fro connecting to database
- a base person class that is going to be used as inheritance for Teacher class and Student Class since every person should have name, age and email 
- Class Class for managing Class ID , class capacity and Class name
- Class Students
- Class Teacher
- Class Course
- Class Reporting : this class contains 2 parts part1 for CSV Reports and part2 for vizualization
## main.py
This file contains the main menu code. The manu is made for easier use of the program (database_sys.py)
- Main menu: provides 6 options and the first 5 options has their own menu with other diffrent options.
