import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pymongo import MongoClient

#################################
# user input order: 
# 1. classes   2. person (students, teachers)  3. courses
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
class DB_connection:
    def __init__(self, user, password, host, database, logger):
        self.client = MongoClient(host, username=user, password=password)
        self.db = self.client[database]
        self.logger = logger

    def close(self):
        self.client.close()
        self.logger.write_log("close", "Database connection closed")

    def execute_query(self, collection_name, operation, data=None):
        try:
            collection = self.db[collection_name]
            if operation == 'insert':
                result = collection.insert_one(data)
                self.logger.write_log("insert", "Data inserted successfully")
                return result.inserted_id
            elif operation == 'delete':
                result = collection.delete_one(data)
                self.logger.write_log("delete", "Data deleted successfully")
                return result.deleted_count
            elif operation == 'update':
                result = collection.update_one(data[0], {"$set": data[1]})
                self.logger.write_log("update", "Data updated successfully")
                return result.modified_count
            elif operation == 'find':
                result = collection.find(data)
                self.logger.write_log("find", "Data retrieved successfully")
                return list(result)
        except Exception as e:
            self.logger.write_log("execute_query", f"Error executing query: {e}")
            print(f"Error executing query: {e}")

#.........................................................................................................               
########>>>>>>>>>>>>>>> base class for any PERSON in the system <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<               
class Person:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age  

    def __str__(self):
        return f"Person name: {self.name}, {self.age} years old, with email: {self.email}"  

#.................................................................................................                      
class Class:
    def __init__(self, db, class_id, class_name, class_capacity):
        if not isinstance(class_capacity, int) or class_capacity < 0:
            raise ValueError("Invalid class capacity! Must be a positive number!")
        self.db = db 
        self.class_name = class_name 
        self.class_id = class_id
        self.class_capacity = class_capacity

    def add_class(self):
        data = {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "class_capacity": self.class_capacity
        }
        self.db.execute_query("classes", "insert", data)
        print(f"\nClass '{self.class_name}' added successfully, ID: {self.class_id}")

    def remove_class(self, class_id):
        result = self.db.execute_query("classes", "delete", {"class_id": class_id})
        if result:
            print(f"\nClass ID: '{class_id}' removed successfully!")

    def edit_class(self, class_id, field, value):
        if field not in ["class_name", "class_capacity"]:
            raise ValueError(f"Invalid field '{field}' provided for update!")

        data = [{"class_id": class_id}, {field: value}]
        self.db.execute_query("classes", "update", data)
        print(f"\nClass: '{class_id}' updated!")

    def search_class(self, class_id):
        result = self.db.execute_query("classes", "find", {"class_id": class_id})
        if result:
            for row in result:
                print(f"\nClass ID: {row['class_id']}, Name: {row['class_name']}, Capacity: {row['class_capacity']}")
        else:
            print(f"\nNo class found with ID: {class_id}")

    def is_class_id_valid(self, class_id):
        result = self.db.execute_query("classes", "find", {"class_id": class_id})
        return len(result) > 0

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..................... Student class
class Student(Person, Class):
    def __init__(self, db, name, grade, email, age, student_id, class_id):
        super().__init__(name, email, age)
        Class.__init__(self, db, class_id, "", 0)

        if not isinstance(age, int) or not isinstance(grade, int) or grade > 100 or grade < 0 or age < 5 or age > 30:
            raise ValueError("Invalid Age or Grade Number!")
         
        self.student_id = student_id 
        self.grade = grade
        self.class_id = class_id 
    #........................................................
    def add_stu(self):
        if not self.is_class_id_valid(self.class_id):
            raise ValueError(f"ID Error: Invalid Class ID '{self.class_id}'!")
        
        data = {
            "student_id": self.student_id,
            "name": self.name,
            "grade": self.grade,
            "email": self.email,
            "age": self.age,
            "class_id": self.class_id
        }
        self.db.execute_query("students", "insert", data)
        print(f"\nStudent added successfully! Student ID: {self.student_id}")
     #......................................................................
    def remove_stu(self, student_id):
        result = self.db.execute_query("students", "delete", {"student_id": student_id})
        if result:
            print(f"\nStudent {student_id} removed!")
    #..............................................................................
    def edit_stu(self, student_id, field, value):
        if field not in ["name", "grade", "email", "age", "class_id"]:
            raise ValueError(f"Invalid field '{field}' provided for update.")

        data = [{"student_id": student_id}, {field: value}]
        self.db.execute_query("students", "update", data)
        print("\nStudent updated")
    #.................................................................................
    def search_stu(self, student_id):
        result = self.db.execute_query("students", "find", {"student_id": student_id})
        if result:
            print("\nStudent found:")
            for row in result:
                print(f"Student ID: {row['student_id']}, Name: {row['name']}, Grade: {row['grade']}, Email: {row['email']}, Age: {row['age']}, Class ID: {row['class_id']}")
        else:
            print(f"\nStudent ID '{student_id}' not found!")
    #..........................................................valid or no
    def is_student_id_valid(self, student_id):
        result = self.db.execute_query("students", "find", {"student_id": student_id})
        return len(result) > 0 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..................................... Teacher class
class Teacher(Person, Class):
    def __init__(self, db, name, email, age, teacher_id, class_id):
        super().__init__(name, email, age)
        Class.__init__(self, db, class_id, "", 0)
        
        self.teacher_id = teacher_id  
        self.course_id = None
        self.class_id = class_id

    def add_t(self):
        if not self.is_class_id_valid(self.class_id):
            raise ValueError(f"ID Error: Invalid Class ID '{self.class_id}'!")
        
        if not isinstance(self.age, int) or self.age < 20 or self.age > 60:
            raise ValueError("Invalid age! Teacher age must be between 20 to 60!") 
             
        data = {
            "teacher_id": self.teacher_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "class_id": self.class_id,
            "course_id": self.course_id
        }
        self.db.execute_query("teachers", "insert", data)
        print("Teacher added successfully!")
     #.....................................................................
    def remove_t(self, teacher_id):
        result = self.db.execute_query("teachers", "delete", {"teacher_id": teacher_id})
        if result:
            print(f"Teacher {teacher_id} removed !")
     #....................................................................
    def edit_t(self, teacher_id, field, value):
        if field not in ["name", "email", "age", "course_id", "class_id"]:
            raise ValueError(f"Invalid field '{field}' provided for update! ! ")
        
        data = [{"teacher_id": teacher_id}, {field: value}]
        self.db.execute_query("teachers", "update", data)
        print("\nTeacher updated")
     #....................................................................
    def search_t(self, teacher_id):
        result = self.db.execute_query("teachers", "find", {"teacher_id": teacher_id})
        if result:
            print("\nTeacher Found:")
            for row in result:
                print(f"Teacher ID: {row['teacher_id']}, Name: {row['name']}, Email: {row['email']}, Age: {row['age']}, Class ID: {row['class_id']}, Course ID: {row['course_id']}")
        else:
            print(f"\nTeacher ID '{teacher_id}' not found!")
    #.......................................................................................
    def is_teacher_valid(self, teacher_id):
        result = self.db.execute_query("teachers", "find", {"teacher_id": teacher_id})
        return len(result) > 0 

#>>>>>>>>>>......................................................................>>>> Course class
class Course(Class):
    def __init__(self, db, course_name, total_hours, course_id, teacher_id, class_id):  
        Class.__init__(self, db, class_id, "", 0)
        self.db = db 
        self.course_name = course_name
        self.total_hours = total_hours 
        self.course_id = course_id
        self.class_id = class_id
        self.teacher_id = teacher_id  

    def add_course(self):
        if self.is_course_id_valid(self.course_id):
            raise ValueError(f"ID Error: Course ID '{self.course_id}' already exists!")

        if not self.is_teacher_valid(self.teacher_id):
            raise ValueError(f"ID Error: Invalid Teacher ID '{self.teacher_id}'!")

        if not self.is_class_id_valid(self.class_id):
            raise ValueError(f"ID Error: Invalid Class ID '{self.class_id}'!")

        if not isinstance(self.total_hours, int) or self.total_hours <= 0:
            raise ValueError("Invalid total hours! It must be a positive integer!")

        data = {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "total_hours": self.total_hours,
            "teacher_id": self.teacher_id,
            "class_id": self.class_id
        }
        self.db.execute_query("courses", "insert", data)
        
        #>>>>>>>>>>>> Update teachers too <<<<<<<<<<
        self.db.execute_query("teachers", "update", [{"teacher_id": self.teacher_id}, {"course_id": self.course_id}])
        
        print(f"\nCourse '{self.course_name}' (ID: {self.course_id}) added successfully!")
     #..................................................................................
    def remove_course(self, course_id):
        result = self.db.execute_query("courses", "delete", {"course_id": course_id})
        if result:
            print(f"\nCourse ID '{course_id}' removed successfully.")
     #.......................................................................................
    def edit_course(self, course_id, field, value):
        if field not in ["course_name", "total_hours", "teacher_id", "class_id"]:
            raise ValueError(f"Invalid field '{field}'!")

        data = [{"course_id": course_id}, {field: value}]
        self.db.execute_query("courses", "update", data)
        print(f"\nCourse ID '{course_id}' updated successfully!")
    #....................................................................................
    def search_course(self, course_id):
        result = self.db.execute_query("courses", "find", {"course_id": course_id})
        if result:
            print("\nCourse Found:")
            for row in result:
                print(f"Course ID: {row['course_id']}, Name: {row['course_name']}, Total Hours: {row['total_hours']}, Teacher ID: {row['teacher_id']}, Class ID: {row['class_id']}")
        else:
            print(f"\nCourse: {course_id} Not found!")
    #......................................................................................
    def is_course_id_valid(self, course_id):
        result = self.db.execute_query("courses", "find", {"course_id": course_id})
        return len(result) > 0

    def is_teacher_valid(self, teacher_id):
        result = self.db.execute_query("teachers", "find", {"teacher_id": teacher_id})
        return len(result) > 0

    def is_class_id_valid(self, class_id):
        result = self.db.execute_query("classes", "find", {"class_id": class_id})
        return len(result) > 0  

# >>>>>>>>>>>>>>>>>..........................................Reporting class
class Reporting:
    def __init__(self, db):
        self.db = db

    def execute_query(self, collection_name, operation, params=None):
        try:
            return self.db.execute_query(collection_name, operation, params)
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    # ------------>>>>>>>>>>>>>-------- CSV Reports ------<<<<<<<<<<<<<<<<<<--------------
    def class_summary_report(self, filename="class_summary.csv"):
        data = self.execute_query("classes", "find")
        if data:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            print(f"\nClass summary report saved to {filename}")
        else:
            print("\nNo data found for class summary report !")

    def teacher_workload_report(self, filename="teacher_workload.csv"):
        pipeline = [
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "teacher_id",
                    "foreignField": "teacher_id",
                    "as": "courses"
                }
            },
            {
                "$lookup": {
                    "from": "students",
                    "localField": "class_id",
                    "foreignField": "class_id",
                    "as": "students"
                }
            },
            {
                "$group": {
                    "_id": "$teacher_id",
                    "name": {"$first": "$name"},
                    "total_courses": {"$size": "$courses"},
                    "total_students": {"$sum": {"$size": "$students"}}
                }
            }
        ]
        data = self.db.db.teachers.aggregate(pipeline)
        df = pd.DataFrame(list(data))
        if not df.empty:
            df.to_csv(filename, index=False)
            print(f"Teacher workload report saved to {filename}.")
        else:
            print("No data found !~")

    def student_performance_report(self, filename="student_performance.csv"):
        pipeline = [
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "class_id",
                    "foreignField": "class_id",
                    "as": "courses"
                }
            }
        ]
        data = self.db.db.students.aggregate(pipeline)
        df = pd.DataFrame(list(data))
        if not df.empty:
            df.to_csv(filename, index=False)
            print(f"Student performance report saved to {filename}")
        else:
            print("No data found !! ")

    def enrollment_trends_report(self, filename="enrollment_trends.csv"):
        pipeline = [
            {
                "$group": {
                    "_id": {"$year": "$created_at"},
                    "total_students": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]
        data = self.db.db.students.aggregate(pipeline)
        df = pd.DataFrame(list(data))
        if not df.empty:
            df.to_csv(filename, index=False)
            print(f"Enrollment trends report saved to {filename} ! !")
        else:
            print("No data found ! ! ")

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ------ >>>>>>>  Data Visualization <<<<<<<<<<--------
    def display_enrollment_trends(self):
        pipeline = [
            {
                "$group": {
                    "_id": {"$year": "$created_at"},
                    "total_students": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]
        data = self.execute_query("students", "aggregate", pipeline)
        if data:
            df = pd.DataFrame(data)
            plt.figure(figsize=(10, 6))
            plt.plot(df["_id"], df["total_students"], marker="o", linestyle="-", color="b")
            plt.title("Enrollment Trends Over Time")
            plt.xlabel("Year")
            plt.ylabel("Total Students")
            plt.grid(True)
            plt.show()
        else:
            print("\nNo data available ! !")

    def analyze_teacher_workload(self):
        pipeline = [
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "teacher_id",
                    "foreignField": "teacher_id",
                    "as": "courses"
                }
            },
            {
                "$lookup": {
                    "from": "students",
                    "localField": "class_id",
                    "foreignField": "class_id",
                    "as": "students"
                }
            },
            {
                "$group": {
                    "_id": "$name",
                    "total_courses": {"$sum": {"$size": "$courses"}},
                    "total_students": {"$sum": {"$size": "$students"}}
                }
            }
        ]
        data = self.db.db.teachers.aggregate(pipeline)
        df = pd.DataFrame(list(data))

        if not df.empty:
            x = np.arange(len(df["_id"]))
            width = 0.35

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(x - width / 2, df["total_courses"], width, label="Courses")
            ax.bar(x + width / 2, df["total_students"], width, label="Students")

            ax.set_xlabel("Teachers")
            ax.set_ylabel("Count")
            ax.set_title("Teacher Workload Analysis")
            ax.set_xticks(x)
            ax.set_xticklabels(df["_id"], rotation=45, ha="right")
            ax.legend()

            plt.tight_layout()
            plt.show()
        else:
            print("\nNo data available to analyze teacher workload ! !   !")
     #..........................................................................
    def summarize_student_performance(self, student_id):
        pipeline = [
            {
                "$match": {"student_id": student_id}
            },
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "class_id",
                    "foreignField": "class_id",
                    "as": "courses"
                }
            }
        ]
        data = self.execute_query("students", "aggregate", pipeline)
        if data:
            df = pd.DataFrame(data)
            plt.figure(figsize=(10, 6))
            plt.plot(df["course_name"], df["grade"], marker="o")
            plt.title(f"Performance of Student ID: {student_id}")
            plt.xlabel("Courses")
            plt.ylabel("Grades")
            plt.grid(True)
            plt.show()
        else:
            print(f"No performance data for: {student_id} !!!!!!")