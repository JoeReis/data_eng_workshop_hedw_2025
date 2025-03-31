-- Create table for students (basic details)
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    email VARCHAR(100) UNIQUE,
    admission_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for courses
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(10) NOT NULL UNIQUE,
    course_title VARCHAR(100) NOT NULL,
    course_description TEXT,
    credits INT CHECK (credits > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for professors
CREATE TABLE professors (
    professor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for student admissions (additional details)
CREATE TABLE student_admissions (
    admission_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    program VARCHAR(100) NOT NULL,
    admission_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for enrollments (mapping students to courses)
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for course assignments (linking courses with professors)
CREATE TABLE course_assignments (
    assignment_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL,
    professor_id INT NOT NULL,
    assigned_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);