import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from langchain_ollama.llms import OllamaLLM
from sqlalchemy import create_engine
import ast