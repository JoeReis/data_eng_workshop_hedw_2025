# 🛠️ Data Engineering Lab: Building a Modern Data and AI Pipeline, HEDW 2025

Welcome to the lab! The goal of this lab is to explore parts of the data enginering lifecycle using open-source tools. You'll learn traditional data pipeline and transformation and dive into using AI to query your data warehouse.

You will:

- Create tables and data in a Postgres database.
- Extract data from the Postgres source database.
- Ingest data efficiently using Data Load Tool (dlt).
- Store and manage data within DuckDB.
- Develop a Kimball-style dimensional model using SQL.
- Serve the modeled data interactively via a Streamlit application.
- Experiment with AI querying capabilities using Ollama, Llama, and LangChain, presented through another Streamlit app.

This lab is part of a broader full-day data engineering workshop.

🎯 Learning Goals

By the end of this lab, you will:
- Understand how to use dlt to extract and load data into DuckDB
- Create a simple data warehouse for analytics and reporting
- Use Streamlit to build a simple data app
- Use AI tools LangChain and Ollama to generate SQL from natural language

🧰 Tools & Technologies
- PostgreSQL – Source system
- DLT (Data Load Tool) – Ingestion framework
- DuckDB – Analytical storage engine
- SQL – Data transformation and modeling
- Python – Pipeline and app development
- Streamlit – Interactive data application
- Ollama + LangChain – Text-to-SQL interface via LLMs

🖥️ Environment Setup

This workshop runs entirely in GitHub Codespaces. No local setup is required.
Note - there might be a small cost to run GitHub Codespaces.

1.	Open the lab repository in your browser.
2.	Click “Code” > “Codespaces” > “Create codespace on main”.
3.	Wait for the Codespace to initialize. This should take a few minutes to spin up.

🧪 Lab Instructions

Each step contains descriptions, hints, and blanks for you to fill in with code.

## Source Systems

In this lab, we'll use PostgresSQL as our source database. PostgreSQL (often referred to as Postgres) is a powerful, open-source relational database management system (RDBMS) known for its reliability, feature richness, and standards compliance. Some call it the "Swiss Army Knife" of databases, due to its vast extension ecosystem. Postgres organizes data into tables with rows and columns, and allows you to query and manipulate that data using SQL (Structured Query Language). Postgres is designed to handle everything from small single-machine applications to large-scale, multi-user systems, and it supports advanced features like full-text search, custom data types, JSON support, and transactional integrity. Because of its flexibility and performance, Postgres is widely used in both traditional and modern data architectures as a source system for analytical pipelines. For our purposes, we'll use Postgres as a typical OLTP database that stores various records related to enrollment, students, professors, and so on.

### Create Tables and Load Data

create tables and load table

query

## Storage

duckdb

what's the difference?


## Data Ingestion


## Data Modeling and Transformation

## Serving Data for Analytics and AI

🧹 Cleanup (Optional)

If you’d like to stop your Codespace and avoid using more GitHub credits:
- Click the “Codespaces” tab in GitHub
- Stop or delete your session



