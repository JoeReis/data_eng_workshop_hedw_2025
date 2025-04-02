import streamlit as st
import duckdb

conn = duckdb.connect(database='university_data.duckdb', read_only=True)

st.title('DuckDB Streamlit App')
st.write('This is a simple Streamlit app that queries a DuckDB database.')

st.subheader('Query Student Dimension Table')
st.write('The database is read-only and contains a table called "dim_students". Let\'s have a look at that table.')

query = f"""
SELECT * FROM serving.dim_students
"""

st.dataframe(conn.execute(query).fetchdf())
st.write('The above table shows all the students in the data warehouse.')

