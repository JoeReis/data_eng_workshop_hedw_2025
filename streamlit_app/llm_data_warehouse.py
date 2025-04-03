import streamlit as st
from langchain_core.prompts import PromptTemplate
# No longer need SQLDatabase for execution, only for potential schema info later
# from langchain_community.utilities import SQLDatabase
from langchain_ollama.llms import OllamaLLM
from sqlalchemy import create_engine
import ast
import re
import pandas as pd

# --- Renamed function to reflect it returns the engine ---
@st.cache_resource
def get_engine():
    # Create and return the SQLAlchemy engine directly
    engine = create_engine("duckdb:///university_data.duckdb")
    return engine

@st.cache_resource
def get_llm():
    return OllamaLLM(
        model="llama3.2",
        temperature=0,
        top_p=0.5,
        num_ctx=1024
    )

st.title("LangChain with Streamlit for DuckDB")
st.write("Ask a question, get SQL, see results.")

# --- Get the cached engine ---
db_engine = get_engine()
llm = get_llm()

# Define the prompt template for SQL generation
sql_prompt_template = """
You are a DuckDB SQL expert. Given a question, generate ONLY a syntactically correct DuckDB SQL query.
Pay attention to the following database schema:
Schema: serving
Tables:
- dim_students (course_sk, student_id, student_name, major, ...)
- dim_courses (course_sk, course_id, course_title, department, ...)
- dim_professors (professor_sk, professor_id, professor_name, department, ...)
- fact_enrollments (enrollment_sk, student_sk, course_sk, enrollment_date_key, date_sk, created_at, ...)
- fact_course_assignments (assignment_sk, professor_sk, course_sk, term_id, date_sk, created_at, ...)
- dim_date (day, date, month, year, semester...)

Instructions:
1. Generate ONLY SELECT statements.
2. Prefix table names with the schema 'serving.' in the FROM and JOIN clauses (e.g., FROM serving.fact_enrollments AS E).
3. When table aliases (like 'AS E', 'AS C') are used in FROM/JOIN, **you MUST use these aliases to refer to columns** in the SELECT, WHERE, GROUP BY, and ORDER BY clauses (e.g., SELECT C.name, COUNT(E.enrollment_id) ... WHERE C.department = '...'). Do NOT use the full schema-qualified name like 'serving.dim_courses.name' when an alias exists.
4. Do NOT use quotes around schema-qualified table names in the FROM/JOIN clauses (e.g., use serving.dim_courses, NOT "serving.dim_courses").
5. Keep queries simple and efficient for DuckDB.
5. Join on sk, not id.
7. MOST IMPORTANT: Your response MUST be ONLY the SQL query, with NO introductory text, explanations, notes, or 'Answer:' prefixes. End the query with a semicolon (;).

Question: {query}

SQL Query:
"""
sql_prompt = PromptTemplate.from_template(sql_prompt_template)

def fix_sql_syntax(sql_query):
    if not isinstance(sql_query, str):
        return sql_query
    sql_query = re.sub(r"```sql\n(.*)\n```", r"\1", sql_query, flags=re.DOTALL)
    sql_query = re.sub(r"```(.*)```", r"\1", sql_query, flags=re.DOTALL)
    select_pos = sql_query.upper().find("SELECT")
    if select_pos > 0:
        sql_query = sql_query[select_pos:]
    if ';' in sql_query:
        sql_query = sql_query.split(';')[0] + ';'
    else:
        sql_query = sql_query.strip() + ';'
    fixed_sql = re.sub(r'"([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)"', r'\1.\2', sql_query)
    return fixed_sql.strip()

st.subheader("Enter your query:")
user_query = st.text_input("Your question:")

if user_query:
    with st.spinner("Generating SQL and querying the database..."):
        try:
            # --- Step 1: Generate SQL ---
            formatted_prompt = sql_prompt.format(query=user_query)
            @st.cache_data(ttl=60)
            def generate_sql(prompt_text):
                # Use the globally available llm object
                return llm.invoke(prompt_text)
            raw_sql_response = generate_sql(formatted_prompt)
            st.subheader("Raw LLM Response (Should be SQL):")
            st.text(raw_sql_response)

            # --- Step 2: Clean SQL ---
            fixed_sql = fix_sql_syntax(raw_sql_response)
            st.subheader("Cleaned SQL Query:")
            st.code(fixed_sql, language="sql")

            # --- Step 3: Execute SQL ---
            # Modify execute_query to accept the engine
            @st.cache_data(ttl=300)
            def execute_query(sql, _engine_to_use): # Pass engine as argument
                try:
                    # Use the passed engine directly
                    with _engine_to_use.connect() as connection:
                        result_df = pd.read_sql(sql, connection)
                        return result_df
                except Exception as e:
                    raise ValueError(f"SQL execution error: {e}\nProblematic SQL:\n{sql}")

            # Pass the db_engine to the function
            query_result_df = execute_query(fixed_sql, db_engine)

            # --- Step 4: Display Results ---
            st.subheader("Query Result:")
            if isinstance(query_result_df, pd.DataFrame):
                st.dataframe(query_result_df)
            else:
                st.write(query_result_df)

        except ValueError as ve:
             st.error(str(ve))
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.exception(e)