import streamlit as st
import duckdb

conn = duckdb.connect(database='university_data.duckdb', read_only=True)
#conn.execute("SET schema 'serving'")  # <- only works if you want to run queries without schema prefix

st.title('DuckDB Streamlit App')
st.write('This is a simple Streamlit app that queries a DuckDB database.')
st.write('The database is read-only and contains a table called "dim_students". Let\'s have a look at that table.')

choose_id = st.selectbox("Choose a student id", range(1, 19))

query = f"""
SELECT * FROM 'serving.dim_students'
"""

st.dataframe(conn.execute(query).fetchdf())
st.write('The above table shows all the students in the database.')