
-- === DIMENSION TABLE MIGRATIONS WITH SCD TYPE 2 ===

-- STUDENTS (SCD Type 2)
INSERT INTO serving.dim_students (
    student_sk, student_id, first_name, last_name, email, date_of_birth, admission_date,
    effective_date, end_date, is_current
)
SELECT
    row_number() OVER () AS student_sk,
    s.student_id,
    s.first_name,
    s.last_name,
    s.email,
    s.date_of_birth,
    s.admission_date,
    CURRENT_TIMESTAMP AS effective_date,
    NULL AS end_date,
    TRUE AS is_current
FROM students s;

-- COURSES (SCD Type 2)
INSERT INTO serving.dim_courses (
    course_sk, course_id, course_code, course_title, course_description, credits,
    effective_date, end_date, is_current
)
SELECT
    row_number() OVER () AS course_sk,
    c.course_id,
    c.course_code,
    c.course_title,
    c.course_description,
    c.credits,
    CURRENT_TIMESTAMP AS effective_date,
    NULL AS end_date,
    TRUE AS is_current
FROM courses c;

-- PROFESSORS (SCD Type 2)
INSERT INTO serving.dim_professors (
    professor_sk, professor_id, first_name, last_name, email, department,
    effective_date, end_date, is_current
)
SELECT
    row_number() OVER () AS professor_sk,
    p.professor_id,
    p.first_name,
    p.last_name,
    p.email,
    p.department,
    CURRENT_TIMESTAMP AS effective_date,
    NULL AS end_date,
    TRUE AS is_current
FROM professors p;

-- === DATE DIMENSION ===

-- Generate a date range for the entire year of 2024
INSERT INTO serving.dim_date (date, day, month, year, quarter, semester)
SELECT
    d,
    EXTRACT(day FROM d),
    EXTRACT(month FROM d),
    EXTRACT(year FROM d),
    EXTRACT(quarter FROM d),
    CASE
        WHEN EXTRACT(month FROM d) BETWEEN 1 AND 6 THEN 'Spring'
        ELSE 'Fall'
    END AS semester
FROM generate_series(DATE '2024-01-01', DATE '2024-12-31', INTERVAL 1 day) AS d;

-- === FACT TABLE MIGRATIONS ===

-- ENROLLMENTS FACT
INSERT INTO serving.fact_enrollments (
    enrollment_sk, student_sk, course_sk, date_sk, created_at
)
SELECT
    e.enrollment_id AS enrollment_sk,
    ds.student_sk,
    dc.course_sk,
    e.enrollment_date AS date_sk,
    CURRENT_TIMESTAMP AS created_at
FROM enrollments e
JOIN dim_students ds ON e.student_id = ds.student_id AND ds.is_current = TRUE
JOIN dim_courses dc ON e.course_id = dc.course_id AND dc.is_current = TRUE;

-- COURSE ASSIGNMENTS FACT
INSERT INTO serving.fact_course_assignments (
    assignment_sk, course_sk, professor_sk, date_sk, created_at
)
SELECT
    ca.assignment_id AS assignment_sk,
    dc.course_sk,
    dp.professor_sk,
    ca.assigned_date AS date_sk,
    CURRENT_TIMESTAMP AS created_at
FROM course_assignments ca
JOIN dim_courses dc ON ca.course_id = dc.course_id AND dc.is_current = TRUE
JOIN dim_professors dp ON ca.professor_id = dp.professor_id AND dp.is_current = TRUE;
