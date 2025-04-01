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
- Ollama + LLama3.2 + LangChain – Text-to-SQL interface via LLMs

🖥️ Environment Setup

This workshop runs entirely in GitHub Codespaces. No local setup is required.
Note - there might be a small cost to run GitHub Codespaces.

1.	Open the lab repository in your browser.
2.	Click “Code” > “Codespaces” > “Create codespace on main”.
3.	Wait for the Codespace to initialize. This should take a few minutes to spin up.

🧪 Lab Instructions

Each step contains descriptions, hints, and blanks for you to fill in with code.

_WARNING_ - Whatever you do, do _NOT_ exit codespaces or shutdown ports that are running. Doing so will force you to start the entire lab over.

## Source Systems

In this lab, we'll use PostgresSQL as our source database. PostgreSQL (often referred to as Postgres) is a powerful, open-source relational database management system (RDBMS) known for its reliability, feature richness, and standards compliance. Some call it the "Swiss Army Knife" of databases, due to its vast extension ecosystem. Postgres organizes data into tables with rows and columns, and allows you to query and manipulate that data using SQL (Structured Query Language). Postgres is designed to handle everything from small single-machine applications to large-scale, multi-user systems, and it supports advanced features like full-text search, custom data types, JSON support, and transactional integrity. Because of its flexibility and performance, Postgres is widely used in both traditional and modern data architectures as a source system for analytical pipelines. For our purposes, we'll use Postgres as a typical OLTP database that stores various records related to enrollment, students, professors, and so on.

### Create Tables and Load Data

Postgres Database Creation

1. Open the Postgres command line interface (cli). In the command li`ne, type `psql -U postgres`
2. Next, let's create the database. `CREATE DATABASE university;`
3. Connect to the university database `\c university;`

Create Tables

1. Open the pg_scripts folder
2. Open the create_tables_pg.sql file. Select all and copy.
3. Paste the code into the Postgres shell `university=#` prompt. Hit Enter.
4. Verify the tables are in Postgres using the `\dt` command.

Load Data

1. In the pg_scripts folder, open the insert_data_pg.sql file.
2. Select all and copy.
3. Paste the code into the Postgres shell `university=#` prompt. Hit Enter.

Let's verify the data is in the database with a couple of sample queries.

This query should show 100 students.

`SELECT COUNT(*) FROM students;`

And this query 

`SELECT * FROM courses LIMIT 5;`

should list the following classes

- Intro to Computer Science
- Advanced English Literature
- General Biology
- Principles of Economics
- Linear Algebra

You can choose to exit the Postgres terminal or keep the terminal tab open for now.

To exit the Postgres terminal, type `\q`.

Ok. Our source database is set up. Let's next move to Storage.

## Storage

There are too many storage options to count when it comes to consuming data from upstream OLTP databases, streams, and more. In this example, we'll use the very popular DuckDB database.



duckdb

what's the difference?


## Data Ingestion


## Data Modeling and Transformation

## Serving Data for Analytics and AI

🧹 Cleanup (Optional)

If you’d like to stop your Codespace and avoid using more GitHub credits:
- Click the “Codespaces” tab in GitHub
- Stop or delete your session



