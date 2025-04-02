import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from langchain_ollama.llms import OllamaLLM
from sqlalchemy import create_engine
import ast

# Create a SQLAlchemy engine for DuckDB
engine = create_engine("duckdb:///university_data.duckdb")

st.title("LangChain with Streamlit")
st.write("This is a simple Streamlit app that uses LangChain to generate queries for DuckDB.")

# Initialize your model
model = OllamaLLM(model="llama3.2")

# Create a SQLDatabase object with the specified schema and tables.
db = SQLDatabase(engine, schema="serving", include_tables=["dim_students"])

# Create the chain with more parameters for better control
db_chain = SQLDatabaseChain.from_llm(
    llm=model,
    db=db,
    verbose=True,
    return_direct=True  # Return the result directly  # Set temperature to 0 for deterministic output
)

st.title("Streamlit + LangChain + DuckDB Demo")
st.write("Enter a natural language query to search your DuckDB database:")

user_query = st.text_input("Your query:")

if user_query:
    st.write("Processing your query...")
    try:
        # Use the invoke method with a dictionary
        result = db_chain.invoke({"query": user_query})
        
        # Get the result from the dictionary
        raw_result = result.get("result", "")
        
        # Remove any unwanted leading prefix
        if raw_result.lower().startswith("sql"):
            raw_result = raw_result[3:].strip()
        
        # Clean approach to extract the value
        try:
            # Try to safely evaluate the string representation of the result
            # This converts a string like "[(20,)]" to a Python list containing a tuple
            parsed_result = ast.literal_eval(raw_result)
            
            if parsed_result and isinstance(parsed_result, list) and len(parsed_result) > 0:
                # Extract the first value from the first tuple
                value = parsed_result[0][0] if parsed_result[0] else None
                
                # Format the result in natural language
                if "how many" in user_query.lower() and value is not None:
                    formatted_result = f"There are {value} students in the database."
                else:
                    formatted_result = f"Result: {value}"
            else:
                formatted_result = f"Result: {raw_result}"
        except (ValueError, SyntaxError, TypeError):
            # If parsing fails, just show the raw result
            formatted_result = f"Result: {raw_result}"
        
        st.write("### Query Result")
        st.write(formatted_result)
        
        # Optionally show the raw result
        with st.expander("Raw response"):
            st.write(result)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Error type: {type(e)}")  # This helps debug the exact errorhis helps debug the exact error