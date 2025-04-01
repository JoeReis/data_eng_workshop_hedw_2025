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

When it comes to upstream OLAP databases, there are nearly countless options on the market. In this lab, we're using DuckDB, a very popular and lightweight OLAP database.

🦆 **Why are we using DuckDB in this lab?**

DuckDB is a lightweight, high-performance analytical database that fits perfectly into modern data engineering workflows. Here’s why it’s ideal for this lab:

- **Ease of Use**: DuckDB runs in-process, meaning no server setup or maintenance is required. You can use it directly from your Python scripts or notebooks.
- **Speed**: It’s optimized for analytical queries, enabling fast processing of large datasets.
- **Portability**: DuckDB is self-contained and works across platforms, making it easy to integrate into various environments.
- **SQL Support**: It supports advanced SQL features, allowing you to perform complex transformations and modeling.
- **Scalability**: While lightweight, DuckDB can handle substantial data volumes, making it suitable for both prototyping and production use cases.

🔍 Key Features of DuckDB
- **Fast analytics**: DuckDB is optimized for OLAP (analytical) workloads and columnar data access.
- **In-process**: It runs inside your Python script or notebook—no need to run a separate database server.
- **Easy integration**: Works great with tools like Pandas, dbt, and even Excel or Parquet files.
- **Portable**: The whole database can be saved as a single .duckdb file and moved around easily.

🛠️ In this lab, DuckDB plays the role of a lightweight analytical database where we:
- Load and store data ingested from Postgres using dlt.
- Build dimensional models (like fact and dimension tables) using SQL.
- Query and analyze the data quickly and interactively.
- Power visualizations and LLM-based interfaces without needing a full database server.

Because DuckDB is extremely simple to use, we won't spend a ton of time going through the details. Instead, let's get familiar with DuckDB via the command line.

1. Let's open up DuckDB by typing `duckdb`
2. Generate a simple query `SELECT * FROM generate_series(5);`
3. Find the length of a string `SELECT upper('duckdb is cool'), length('how long is this?');`
4. Do a little math `SELECT 42 * 17 AS answer;`
5. Generate a date range `SELECT * FROM generate_series(date '2025-01-01', date '2025-01-10', interval 1 day);`
6. JSON parsing from raw strings `SELECT json_extract('{"name": "Tina", "role": "engineer"}', '$.role') AS role;`

Exit DuckDB by typing `.exit`

Ok, let's do something more interesting with DuckDB and load some data into it.

## Data Ingestion

Let's use Data Load Tool (dlt) to load data from Postgres to DuckDB.

In the terminal, type `python dlt_pipeline.py`

This will create a DuckDB database called university_data.duckdb

Let's see what's in this database. Thankfully DuckDB offers a new handy UI to inspect the data in DuckDB.

In the terminal, type `duckdb -ui`

`SELECT * FROM stg_university_data.students;`

[  go through some examples of dlt refresh and increamtanl load with insert ]

## Data Modeling and Transformation

[ create a new layer in duckdb - serving with kimball ]

[  go through some examples of dlt refresh and increamtanl load with update ]

[ scd ]

## Serving Data for Analytics and AI

🧹 Cleanup (Optional)

If you’d like to stop your Codespace and avoid using more GitHub credits:
- Click the “Codespaces” tab in GitHub
- Stop or delete your session



