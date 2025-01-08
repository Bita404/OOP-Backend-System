use school_sys;

--  classes
CREATE TABLE IF NOT EXISTS classes (
    class_id VARCHAR(10) PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    class_capacity INT CHECK (class_capacity > 0)
);

--  students
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    grade FLOAT CHECK (grade >= 0 AND grade <= 100),
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT CHECK (age > 0),
    class_id VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
);

--  teachers
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT CHECK (age > 0),
    class_id VARCHAR(10),
    course_id VARCHAR(10),
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE SET NULL
);

--  courses
CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    total_hours INT CHECK (total_hours > 0),
    teacher_id VARCHAR(10),
    class_id VARCHAR(10),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
);
