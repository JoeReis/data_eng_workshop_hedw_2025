import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase
# Remove SQLDatabaseChain import as we'll use the LLM directly for SQL generation
# from langchain_experimental.sql import SQLDatabaseChain 
from langchain_ollama.llms import OllamaLLM
from sqlalchemy import create_engine
import ast
import re
import pandas as pd # Import pandas for display

# Use Streamlit's caching to avoid reloading the database and model
@st.cache_resource
def get_database():
    engine = create_engine("duckdb:///university_data.duckdb")
    # Use specified schema and include tables
    return SQLDatabase(
        engine,
        schema="serving",
        include_tables=["dim_students", "dim_courses", "dim_professors", "fact_enrollments", "fact_course_assignments", "dim_date"],
        sample_rows_in_table_info=0
    )

@st.cache_resource
def get_llm():
    # Configure the LLM
    return OllamaLLM(
        model="llama3.2",
        temperature=0,
        top_p=0.5,
        num_ctx=1024
    )

st.title("LangChain with Streamlit for DuckDB")
st.write("Ask a question, get SQL, see results.")

# Get cached resources
db = get_database()
model = get_llm()

# Define the prompt template for SQL generation
# Added table schema details directly into the prompt for potentially better context
# Emphasized AGAIN to ONLY output SQL.
sql_prompt_template = """
You are a DuckDB SQL expert. Given a question, generate ONLY a syntactically correct DuckDB SQL query.
Pay attention to the following database schema:
Schema: serving
Tables:
- dim_students (student_id, student_name, major, ...)
- dim_courses (course_id, course_name, department, ...)
- dim_professors (professor_id, professor_name, department, ...)
- fact_enrollments (enrollment_id, student_id, course_id, enrollment_date_key, grade, ...)
- fact_course_assignments (assignment_id, professor_id, course_id, term_id, ...)
- dim_date (date_key, date, month, year, ...)

Instructions:
1. Generate ONLY SELECT statements.
2. ALWAYS prefix table names with the schema 'serving.' (e.g., serving.dim_courses).
3. Do NOT use quotes around schema-qualified table names (e.g., use serving.dim_courses, NOT "serving.dim_courses").
4. Keep queries simple and efficient for DuckDB.
5. MOST IMPORTANT: Your response MUST be ONLY the SQL query, with NO introductory text, explanations, notes, or 'Answer:' prefixes. End the query with a semicolon (;).

Question: {query}

SQL Query:
"""

sql_prompt = PromptTemplate.from_template(sql_prompt_template)

# Function to fix common SQL syntax issues - keep this, it's useful!
def fix_sql_syntax(sql_query):
    if not isinstance(sql_query, str):
        return sql_query

    # Remove potential markdown code blocks
    sql_query = re.sub(r"```sql\n(.*)\n```", r"\1", sql_query, flags=re.DOTALL)
    sql_query = re.sub(r"```(.*)```", r"\1", sql_query, flags=re.DOTALL)

    # Remove any text before SELECT (like explanations or "SQL Query:")
    select_pos = sql_query.upper().find("SELECT")
    if select_pos > 0:
        sql_query = sql_query[select_pos:]

    # Remove any text after the first semicolon (like 'Answer:' or other LLM chatter)
    if ';' in sql_query:
        sql_query = sql_query.split(';')[0] + ';'
    else:
        # Ensure it ends with a semicolon if one is missing
        sql_query = sql_query.strip() + ';'

    # Remove quotes around schema.table names (if any slip through)
    fixed_sql = re.sub(r'"([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)"', r'\1.\2', sql_query)

    return fixed_sql.strip()

st.subheader("Enter your query:")
user_query = st.text_input("Your question:")

if user_query:
    with st.spinner("Generating SQL and querying the database..."):
        try:
            # --- Step 1: Generate SQL using the LLM directly ---
            formatted_prompt = sql_prompt.format(query=user_query)
            
            # Use caching for the LLM call if the same query is repeated quickly
            @st.cache_data(ttl=60) # Cache LLM response for 60 seconds
            def generate_sql(prompt_text):
                return model.invoke(prompt_text)

            raw_sql_response = generate_sql(formatted_prompt)

            st.subheader("Raw LLM Response (Should be SQL):")
            st.text(raw_sql_response)

            # --- Step 2: Clean the generated SQL ---
            fixed_sql = fix_sql_syntax(raw_sql_response)
            st.subheader("Cleaned SQL Query:")
            st.code(fixed_sql, language="sql")

            # --- Step 3: Execute the SQL ---
            @st.cache_data(ttl=300) # Cache DB results for 5 minutes
            def execute_query(sql):
                try:
                    with db.engine.connect() as connection:
                        # Use pandas to read sql for better formatting and type handling
                        result_df = pd.read_sql(sql, connection)
                        return result_df
                except Exception as e:
                    # Raise the exception to be caught outside
                    raise ValueError(f"SQL execution error: {e}\nProblematic SQL:\n{sql}")

            query_result_df = execute_query(fixed_sql)

            # --- Step 4: Display Results ---
            st.subheader("Query Result:")
            if isinstance(query_result_df, pd.DataFrame):
                st.dataframe(query_result_df)
            else:
                # Should not happen with pd.read_sql but handle just in case
                st.write(query_result_df)

        except ValueError as ve: # Catch specific SQL execution errors
             st.error(str(ve))
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            # Provide more context for debugging if needed
            st.exception(e)