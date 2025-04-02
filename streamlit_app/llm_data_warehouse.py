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
        include_tables=["dim_students", "dim_courses", "dim_professors", "fact_enrollments"],
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

# Create a minimal prompt that focuses on speed
custom_prompt = """
Given a question, write a simple DuckDB SQL query:
1. Generate ONLY SELECT statements
2. Use schema "serving"
3. Keep queries simple and efficient
4. The query should start with SELECT

Tables: dim_students, dim_courses, dim_professors, fact_enrollments

Question: {query}

SQL Query: SELECT """

PROMPT = PromptTemplate(input_variables=["query"], template=custom_prompt)

# Cache the chain creation
@st.cache_resource
def get_chain():
    return SQLDatabaseChain.from_llm(
        llm=model,
        db=db,
        prompt=PROMPT,
        verbose=False,  # Reduce logging for speed
        return_direct=True
    )

db_chain = get_chain()

st.title("Streamlit + LangChain + DuckDB Demo")
st.write("Enter a natural language query to search your DuckDB database:")

user_query = st.text_input("Your query:")

if user_query:
    # Show a spinner while processing
    with st.spinner("Generating SQL and querying the database..."):
        try:
            # Cache query results to avoid reprocessing the same queries
            @st.cache_data(ttl=300)  # Cache for 5 minutes
            def get_query_result(query):
                return db_chain.invoke({"query": query})
            
            result = get_query_result(user_query)
            raw_result = result.get("result", "")
            
            # Simplify result parsing
            try:
                # Try to format as a table if it looks like tabular data
                if isinstance(raw_result, str) and raw_result.startswith('[') and raw_result.endswith(']'):
                    parsed_result = ast.literal_eval(raw_result)
                    if isinstance(parsed_result, list) and len(parsed_result) > 0:
                        # Show as a table if multiple rows
                        if len(parsed_result) > 1:
                            # Convert to DataFrame if possible
                            import pandas as pd
                            df = pd.DataFrame(parsed_result)
                            st.dataframe(df)
                        else:
                            st.write(f"Result: {parsed_result[0][0] if len(parsed_result[0]) == 1 else parsed_result[0]}")
                    else:
                        st.write(f"Result: {raw_result}")
                else:
                    st.write(f"Result: {raw_result}")
            except:
                st.write(f"Result: {raw_result}")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")