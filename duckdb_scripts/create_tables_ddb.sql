
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
    -- Core Keys
    enrollment_sk BIGINT PRIMARY KEY, -- Surrogate key for the enrollment fact
    student_sk INTEGER NOT NULL,      -- Foreign key to dim_students (Ensured not null)
    course_sk INTEGER NOT NULL,       -- Foreign key to dim_courses (Ensured not null)
    date_sk DATE NOT NULL,            -- Foreign key to dim_date, likely enrollment date (Ensured not null)
    -- Audit Columns
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- Timestamp when the record was created)
);

-- FACT COURSE ASSIGNMENTS
CREATE TABLE serving.fact_course_assignments (
    assignment_sk BIGINT PRIMARY KEY,
    course_sk INTEGER,
    professor_sk INTEGER,
    date_sk DATE,
    -- Audit Columns
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- Timestamp when the record was created

);