
-- STUDENT DIMENSION (SCD Type 2)
CREATE TABLE serving.dim_students (
    student_sk INTEGER PRIMARY KEY,
    student_id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    date_of_birth DATE,
    admission_date DATE,
    effective_date TIMESTAMP,
    end_date TIMESTAMP,
    is_current BOOLEAN
);

-- COURSE DIMENSION (SCD Type 2)
CREATE TABLE serving.dim_courses (
    course_sk INTEGER PRIMARY KEY,
    course_id INTEGER,
    course_code VARCHAR,
    course_title VARCHAR,
    course_description TEXT,
    credits INTEGER,
    effective_date TIMESTAMP,
    end_date TIMESTAMP,
    is_current BOOLEAN
);

-- PROFESSOR DIMENSION (SCD Type 2)
CREATE TABLE serving.dim_professors (
    professor_sk INTEGER PRIMARY KEY,
    professor_id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    department VARCHAR,
    effective_date TIMESTAMP,
    end_date TIMESTAMP,
    is_current BOOLEAN
);

-- TIME DIMENSION
CREATE TABLE serving.dim_date (
    date DATE PRIMARY KEY,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    quarter INTEGER,
    semester VARCHAR
);

-- FACT ENROLLMENTS
CREATE TABLE serving.fact_enrollments (
    enrollment_sk BIGINT PRIMARY KEY,
    student_sk INTEGER,
    course_sk INTEGER,
    date_sk DATE,
    FOREIGN KEY(student_sk) REFERENCES serving.dim_students(student_sk),
    FOREIGN KEY(course_sk) REFERENCES serving.dim_courses(course_sk),
    FOREIGN KEY(date_sk) REFERENCES serving.dim_date(date),
    created_at TIMESTAMP
);

-- FACT COURSE ASSIGNMENTS
CREATE TABLE serving.fact_course_assignments (
    assignment_sk BIGINT PRIMARY KEY,
    course_sk INTEGER,
    professor_sk INTEGER,
    date_sk DATE,
    FOREIGN KEY(course_sk) REFERENCES serving.dim_courses(course_sk),
    FOREIGN KEY(professor_sk) REFERENCES serving.dim_professors(professor_sk),
    FOREIGN KEY(date_sk) REFERENCES serving.dim_date(date),
    created_at TIMESTAMP
);