import streamlit as st
import duckdb

conn = duckdb.connect(database='university_data.duckdb', read_only=True)

st.title('DuckDB Streamlit App')
st.write('This is a simple Streamlit app that queries a DuckDB database.')

st.subheader('Query the Student Dimension Table')
st.write('The database is read-only and contains a table called "dim_students". Let\'s have a look at that table.')

query = f"""
SELECT * FROM serving.dim_students
"""

st.dataframe(conn.execute(query).fetchdf(), key="all_students_table")
st.write('The above table shows all the students in the data warehouse.')

st.subheader('Filter the Student Dimension Table')
st.write('You can filter the table by entering a student ID below.')
student_id = st.text_input('Enter a student ID:', '', key='student_id_input')
if student_id:
    query = f"""
    SELECT * FROM serving.dim_students
    WHERE student_id = '{student_id}'
    """
    st.dataframe(conn.execute(query).fetchdf(), key="filtered_students_table")
else:
    st.write('Please enter a student ID to filter the table.')
    

st.subheader('Let\'s Do Some Analysis')
st.write('We can also do some analysis on the data. For example, let\'s find the top 5 courses with the most enrollments.')

query_top_5_enrollments = f"""SELECT c.course_title, COUNT(*) AS enrollments
FROM serving.fact_enrollments f
JOIN serving.dim_courses c ON f.course_sk = c.course_sk
GROUP BY c.course_title
ORDER BY enrollments DESC
LIMIT 5;"""
st.dataframe(conn.execute(query_top_5_enrollments).fetchdf(), key="top_enrollments_table")

# New section to drill down into course enrollments
st.subheader('Course Enrollment Details')
st.write('Enter a course title to see all students enrolled in that course.')

# Get list of course titles for dropdown
course_titles_query = "SELECT DISTINCT course_title FROM serving.dim_courses ORDER BY course_title;"
course_titles = [row[0] for row in conn.execute(course_titles_query).fetchall()]
selected_course = st.selectbox('Select a course:', [''] + course_titles, key='course_selection')

if selected_course:
    # Query to find students enrolled in the selected course
    enrollment_query = f"""
    SELECT 
        s.first_name, 
        s.last_name, 
        s.email,
        s.admission_date,
        c.course_title,
        c.course_code,
        c.credits
    FROM serving.fact_enrollments f
    JOIN serving.dim_students s ON f.student_sk = s.student_sk
    JOIN serving.dim_courses c ON f.course_sk = c.course_sk
    WHERE c.course_title = '{selected_course}'
    AND s.is_current = TRUE
    AND c.is_current = TRUE
    ORDER BY s.last_name, s.first_name;
    """
    
    enrollment_data = conn.execute(enrollment_query).fetchdf()
    
    if not enrollment_data.empty:
        st.write(f"Found {len(enrollment_data)} students enrolled in '{selected_course}':")
        st.dataframe(enrollment_data, key="course_enrollments_table")
    else:
        st.write(f"No students found enrolled in '{selected_course}'.")