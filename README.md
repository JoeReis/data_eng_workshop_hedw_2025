# 🛠️ Data Engineering Lab: Building a Modern Data and AI Pipeline, HEDW 2025

Welcome! This hands-on lab will walk you through key parts of the modern data engineering lifecycle using open-source tools. You’ll build a traditional analytics pipeline and explore how to query your data warehouse using AI.

By the end, you will have built a small-scale, end-to-end pipeline—from data ingestion to transformation and visualization—with an LLM-powered query interface.

## 🔍 What You’ll Do

- Create tables and data in a Postgres database.
- Extract data from the Postgres source database.
- Ingest data efficiently using Data Load Tool (dlt).
- Store and manage data within DuckDB.
- Develop a Kimball-style dimensional model using SQL.
- Serve the modeled data interactively via a Streamlit application.
- Experiment with AI querying capabilities using Ollama, Llama, and LangChain, presented through another Streamlit app.

This lab is part of a broader full-day data engineering workshop.

## 🎯 Learning Objectives

By the end of this lab, you will:
- Use dlt to extract and load data into DuckDB.
- Create a simple data warehouse for analytics and reporting.
- Build a Streamlit app for exploring your data.
- Use AI tools like LangChain and Ollama to generate SQL from natural language prompts.

## 🧰 Tools & Technologies
- PostgreSQL – Source system (OLTP)
- DLT (Data Load Tool) – Ingestion framework
- DuckDB – Analytical storage engine (OLAP)
- SQL – Data transformation and modeling
- Python – Scripting and app development
- Streamlit – Data visualization and app layer
- Ollama + Llama3.2 + LangChain – LLM-based text-to-SQL interface

## ⚙️ Environment Setup

This lab runs entirely in GitHub Codespaces—no local setup needed!

💡 Note: GitHub Codespaces may incur a small cost depending on your GitHub plan.

1.	Open the lab repository in your browser.
2.	Click “Code” > “Codespaces” > “Create codespace on main”.
3.	Wait a few minutes for the Codespace to initialize.

## 📋 Lab Instructions

Each step includes explanations, hints, and code blanks for you to complete.

⚠️ _WARNING_ - _Do not_ exit your Codespace or shut down running ports unless instructed. Doing so may require you to restart the lab from scratch.

# 🗄️ Source Systems

We’ll start by setting up our source system using PostgreSQL.

PostgreSQL (or “Postgres”) is a powerful open-source relational database management system (RDBMS) known for its flexibility, reliability, and feature-rich extension ecosystem. It’s widely used in both transactional systems and as a source for analytical pipelines.

In this lab, we’ll use Postgres as our operational (OLTP) database, storing mock data for students, professors, enrollment, and more.

## ✅ 1.  Create the Database and Load Tables

Postgres Database Creation

1. Open the Postgres command line interface (CLI). In the command line, type `psql -U postgres`
2. Next, let's create the database. `CREATE DATABASE university;`
3. Confirm the database is created `\l`
4. Connect to the university database `\c university;`

## 🧱 Step 2: Create Tables

1. Open the pg_scripts folder
2. Open the `create_tables_pg.sql` file. Select all and copy.
3. Paste the code into the Postgres shell `university=#` prompt. Hit Enter.
4. Verify the tables are in Postgres using the `\dt` command.

## 📦 Step 3: Insert Data

1. In the pg_scripts folder, open the `insert_data_pg.sql` file.
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

You can now exit the Postgres terminal with: `\q`.

Nice work! Your source database is ready. Next up: storage and ingestion.

# Storage

When it comes to upstream OLAP databases, there are nearly countless options on the market. In this lab, we're using DuckDB, a very popular and lightweight OLAP database.

🦆 **Why are we using DuckDB in this lab?**

DuckDB is a lightweight, high-performance analytical database that fits perfectly into modern data engineering workflows. Here’s why it’s ideal for this lab:

- **Ease of Use**: DuckDB runs in-process, meaning no server setup or maintenance is required. You can use it directly from your Python scripts or notebooks.
- **Speed**: It’s optimized for analytical queries, enabling fast processing of large datasets.
- **Portability**: DuckDB is self-contained and works across platforms, making it easy to integrate into various environments.
- **SQL Support**: It supports advanced SQL features, allowing you to perform complex transformations and modeling.
- **Scalability**: While lightweight, DuckDB can handle substantial data volumes, making it suitable for both prototyping and production use cases.

Key Features of DuckDB
- **Fast analytics**: DuckDB is optimized for OLAP (analytical) workloads and columnar data access.
- **In-process**: It runs inside your Python script or notebook—no need to run a separate database server.
- **Easy integration**: Works great with tools like Pandas, dbt, and even Excel or Parquet files.
- **Portable**: The whole database can be saved as a single .duckdb file and moved around easily.

In this lab, DuckDB plays the role of a lightweight analytical database where we:
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

# Data Ingestion

Let's use Data Load Tool (dlt) to load data from Postgres to DuckDB.

1. Open the file `dlt_pipeline.py`
2. 

In the terminal, type `python dlt_pipeline.py`

This will create a DuckDB database called university_data.duckdb

Let's see what's in this database. Thankfully DuckDB offers a new handy UI to inspect the data in DuckDB.

In the terminal, type `duckdb -ui`

`SELECT * FROM stg_university_data.students;`

[  go through some examples of dlt refresh and incremental load with insert ]

# Data Modeling and Transformation

Create a new schema in DuckDB `CREATE SCHEMA serving;`

[ create a new layer in duckdb - serving with kimball ]

[  go through some examples of dlt refresh and increamtanl load with update ]

[ scd ]

If you have an error loading tables, truncate and start over

TRUNCATE TABLE serving.fact_enrollments;
TRUNCATE TABLE serving.fact_course_assignments;

-- Then truncate dimension tables
TRUNCATE TABLE serving.dim_students;
TRUNCATE TABLE serving.dim_courses; 
TRUNCATE TABLE serving.dim_professors;
TRUNCATE TABLE serving.dim_date;

# Serving Data for Analytics and AI

Now for the fun stuff! You’ve built a pipeline and modeled your data—now it’s time to use that data. In this section, we’ll:

- Build data-powered applications using Streamlit.
- Use large language models (LLMs) to analyze your data and even generate SQL queries.

## Data-Powered Applications in Streamlit

Streamlit is an open-source Python library for building custom web apps for machine learning and data science. It’s perfect for quickly turning data scripts into interactive dashboards and apps—with just a few lines of Python.

Streamlit lets you:
- Display tables, charts, and metrics.
- Create interactive widgets (sliders, dropdowns, text inputs).
- Build full analytics dashboards or internal data tools.

### Let’s Run Your First App

Let's start your first Streamlit app to make sure things are running.

From your terminal in the project directory, type: `streamlit run streamlit_app/hello_world.py`

You should see a web browser window open in `localhost:8501` with a basic Streamlit app that says "hello world".

If you see it—congrats! Your Streamlit environment is working.

Notice the dropdown menu in the top right of the browser. Click it and look around.

### Get to Know Streamlit

Hello world is nice, but pretty boring. Here, we'll look at various ways to use Streamlit. The big thing to notice is how easy it is to build data-powered applications in Streamlit.

Open the file `streamlit_app/basics.py`

From your terminal in the project directory, type: `streamlit run streamlit_app/basics.py`

Let's walk through the exercises.

The solutions to these exercises are located at `streamlit_app/basics_solutions.py`

Now that you've got a good grasp of Streamlit basics, let's connect our streamlit application to our data warehouse.

### Let's Analyze our Data Warehouse

Here, we're going to look at more complex queries and data applications in our data warehouse.

Let’s begin with a simple ranking. This query will show the five courses with the highest number of student enrollments.

`SELECT c.course_title, COUNT(*) AS student_count
FROM fact_enrollments f
JOIN dim_courses c ON f.course_sk = c.course_sk
WHERE c.course_title = 'Intro to Computer Science'
GROUP BY c.course_title;`

Next, let's look how we can filter to the course to determine the number of students per course

First, close Streamlit (Crtl C), then type `streamlit run streamlit_app/duckdb_streamlit.py`

Also, open the file `streamlit_app/duckdb_streamlit.py`

[ make this a fill in the blanks example ]

We've spent some time looking at data-powered applications. How about we look at AI-powered apps?

## AI For Analysis and BI

So far, we’ve explored how data powers analytics and applications — but what happens when we bring AI into the mix?

Let’s shift gears and explore how Large Language Models (LLMs) can enhance analysis, generate insights, and even help us write SQL queries.

### Run the LLM with Ollama

Commercial LLMs are great if you want to interact with their version of the world they've been trained on. What happens if you want to run a model locally to query your internal data.

Thankfully, Ollama provides a great service for downloading models and interacting with them.

We’ll be using Llama 3.2, an open-source language model, to power our AI assistant.

To start the model locally, just run:

Open Llama3.2 `ollama run llama3.2`

Ask Llama3.2 `why is the sky blue?`

You'll probably get a response about molecules and gases interacting with sunlight. The responses will vary because LLMs are probabilistic.

Hit `Ctrl D` to exit llama3.2

### Let's Ask AI About Our Data Warehouse

You saw LLama3.2. It's just an LLM, similar to what you interact with if you ask ChatGPT, Claude, or Gemini questions.

The real power of LLMs is when they're working with YOUR data.

From the terminal, open the file `llms/llm_data_warehouse.py`

Let's look at what's going on.

`what courses have the highest enrollment?`





Langchang - simple example with llama3.2


Text to SQL

# Conclusion

🧹 Cleanup (Optional)

If you’d like to stop your Codespace and avoid using more GitHub credits:
- Click the “Codespaces” tab in GitHub
- Stop or delete your session



