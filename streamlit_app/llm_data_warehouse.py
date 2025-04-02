import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_ollama.llms import OllamaLLM
from sqlalchemy import create_engine
import ast

# Use Streamlit's caching to avoid reloading the database and model
@st.cache_resource
def get_database():
    engine = create_engine("duckdb:///university_data.duckdb")
    # Only include the tables you need and limit sample rows to 0
    return SQLDatabase(
        engine, 
        schema="serving", 
        include_tables=["dim_students", "dim_courses", "dim_professors", "fact_enrollments", "fact_course_assignments", "dim_date"],
        sample_rows_in_table_info=0
    )

@st.cache_resource
def get_llm():
    # Configure the LLM with performance-optimized parameters
    return OllamaLLM(
        model="llama3.2",
        temperature=0,  # More deterministic (faster) responses
        top_p=0.5,      # Sample from smaller probability mass (faster)
        num_ctx=1024    # Smaller context window = faster processing
    )

st.title("LangChain with Streamlit")
st.write("This is a simple Streamlit app that uses LangChain to generate queries for DuckDB.")

# Get cached resources
db = get_database()
model = get_llm()

# Cache the chain creation
@st.cache_resource
def get_chain():
    return SQLDatabaseChain.from_llm(
        llm=model,
        db=db,
        verbose=False,  # Reduce logging for speed
        return_direct=True
    )

db_chain = get_chain()

# Add a function to fix common SQL syntax issues
def fix_sql_syntax(sql_query):
    if not isinstance(sql_query, str):
        return sql_query
        
    # Fix incorrectly quoted schema.table references
    import re
    # Replace patterns like "schema.table" with schema.table
    fixed_sql = re.sub(r'"([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)"', r'\1.\2', sql_query)
    
    # Extract only the SQL part (before any notes or explanations)
    if ';' in fixed_sql:
        fixed_sql = fixed_sql.split(';')[0] + ';'
    
    return fixed_sql.strip()

# Update your prompt to be more explicit
custom_prompt = """
Given a question, write a simple DuckDB SQL query:
1. Generate ONLY SELECT statements
2. Always use schema name 'serving' before table names (example: serving.dim_courses, NOT "serving.dim_courses")
3. Keep queries simple and efficient
4. Do not put quotes around schema-qualified table names
5. IMPORTANT: Your response should ONLY be the SQL query, with no explanations or notes

Tables: serving.dim_students, serving.dim_courses, serving.dim_professors, serving.fact_enrollments

Question: {query}

SQL Query: """

st.title("Streamlit + LangChain + DuckDB Demo")
st.write("Enter a natural language query to search your DuckDB database:")

user_query = st.text_input("Your query:")

if user_query:
    # Show a spinner while processing
    with st.spinner("Generating SQL and querying the database..."):
        try:
            # Create a simpler chain using run method
            @st.cache_data(ttl=300)
            def get_query_result(query):
                # Get raw result from LLM
                result = db_chain.invoke(query)
                
                # Show raw result in an expander
                with st.expander("View raw LLM response"):
                    st.text(result)
                
                # Fix any SQL syntax issues
                if isinstance(result, str):
                    fixed_sql = fix_sql_syntax(result)
                    st.code(fixed_sql, language="sql")
                    
                    try:
                        # Execute the fixed SQL
                        with db.engine.connect() as conn:
                            query_result = conn.execute(fixed_sql).fetchall()
                            return query_result
                    except Exception as e:
                        st.error(f"SQL execution error: {e}")
                        return f"Fixed SQL still has errors: {e}"
                return result
            
            raw_result = get_query_result(user_query)
            
            # Display the result
            st.subheader("Result")
            
            # Simple display logic
            if isinstance(raw_result, str):
                if raw_result.strip().startswith('[') and raw_result.strip().endswith(']'):
                    try:
                        # Try parsing as list/tuple
                        parsed = ast.literal_eval(raw_result)
                        if isinstance(parsed, list) and len(parsed) > 1:
                            # Convert to DataFrame for tabular display
                            import pandas as pd
                            df = pd.DataFrame(parsed)
                            st.dataframe(df)
                        else:
                            st.write(parsed)
                    except:
                        # Fall back to plain text
                        st.write(raw_result)
                else:
                    # Regular string output
                    st.write(raw_result)
            else:
                # Handle non-string results
                st.write(raw_result)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")