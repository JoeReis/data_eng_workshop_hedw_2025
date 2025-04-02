-- total enrollments by Semester by Year

SELECT d.year, d.semester, COUNT(*) AS total_enrollments
FROM serving.fact_enrollments f
JOIN serving.dim_date d ON f.date_sk = d.date
GROUP BY d.year, d.semester
ORDER BY d.year, d.semester;

-- Top 5 Most Popular Courses

SELECT c.course_title, COUNT(*) AS enrollments
FROM serving.fact_enrollments f
JOIN serving.dim_courses c ON f.course_sk = c.course_sk
GROUP BY c.course_title
ORDER BY enrollments DESC
LIMIT 5;

-- Enrollments Per Student

SELECT s.first_name || ' ' || s.last_name AS student_name, COUNT(*) AS courses_enrolled
FROM serving.fact_enrollments f
JOIN serving.dim_students s ON f.student_sk = s.student_sk
GROUP BY student_name
ORDER BY courses_enrolled DESC
LIMIT 10;

--Course Assignments by Professor

SELECT p.first_name || ' ' || p.last_name AS professor_name, COUNT(*) AS courses_taught
FROM serving.fact_course_assignments f
JOIN serving.dim_professors p ON f.professor_sk = p.professor_sk
GROUP BY professor_name
ORDER BY courses_taught DESC;

-- Daily Enrollment Volume

SELECT d.date, COUNT(*) AS daily_enrollments
FROM serving.fact_enrollments f
JOIN serving.dim_date d ON f.date_sk = d.date
GROUP BY d.date
ORDER BY d.date;