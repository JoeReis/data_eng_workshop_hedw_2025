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

⚠️ _WARNING_ - **_Do NOT_** exit your Codespace or shut down running ports unless instructed. Doing so may require you to restart the lab from scratch.

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

## ➡️ Step 3: Insert Data

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

# 🗃️ Storage

When it comes to upstream OLAP databases, there are nearly countless options on the market. In this lab, we're using DuckDB, a lightweight, high-performance OLAP (Online Analytical Processing) database that fits seamlessly into modern data engineering workflows.

## 🦆 Why DuckDB?

DuckDB is a lightweight, high-performance analytical database that fits perfectly into modern data engineering workflows. Here’s why it’s ideal for this lab:

DuckDB has rapidly become a go-to tool for analytics and prototyping. It’s ideal for this lab because it offers:

- Zero Setup – DuckDB runs in-process, directly from your Python scripts or terminal. No servers to manage.
- Speed – Optimized for analytical queries over large datasets.
- Portability – Everything is stored in a single .duckdb file you can move around.
- Flexibility – Compatible with tools like Pandas, Parquet, dbt, and even Excel.
- Rich SQL Support – Full support for complex SQL queries, perfect for dimensional modeling.

✅ In this lab, DuckDB serves as your analytical database:

- It ingests data extracted from Postgres.
- Stores fact and dimension tables.
- Powers both dashboards and AI-driven query interfaces.
- Requires no infrastructure or cloud setup.

Because DuckDB is extremely simple to use, we won't spend a ton of time going through the details. Instead, let's get familiar with DuckDB via the command line.

## 🧪 Try It Out: DuckDB Basics

1. Let's open up DuckDB by typing `duckdb -ui` (if the UI doesn't work, just open up the DuckDB CLI `duckdb`)
2. Generate a series of numbers: `SELECT * FROM generate_series(5);`
3. Find the length of a string: `SELECT upper('duckdb is cool'), length('how long is this?');`
4. Do a little math: `SELECT 42 * 17 AS answer;`
5. Generate a date range: `SELECT * FROM generate_series(date '2025-01-01', date '2025-01-10', interval 1 day);`
6. JSON parsing from raw strings: `SELECT json_extract('{"name": "Tina", "role": "engineer"}', '$.role') AS role;`

Exit DuckDB by typing `.exit`

You just explored some of DuckDB’s built-in features—no server, no config, no friction.

Now that you’ve seen what DuckDB can do, let’s move beyond simple queries. Next, we’ll load real data from our Postgres source using dlt and start modeling it with SQL.

# 🔄 Data Ingestion

In this step, we’ll use dlt (Data Load Tool) to extract data from Postgres and load it into DuckDB.

dlt makes it easy to build declarative data pipelines in Python. You’ll define which Postgres tables to pull, then run the pipeline to ingest the data into a local DuckDB file.

## ⚙️ Step-by-Step Instructions

1. Open the pipeline file. In your Codespace, open: `dlt_pipeline.py`

2. Define the source tables

    As a reminder, we used the following tables:
    - courses
    - course_assignments
    - enrollments
    - professors
    - students
    - student_admissions

    Your code should look like this.

    ```python
    def load_university_pipeline():
        source = sql_database().with_resources(
            "courses",
            "course_assignments",
            "enrollments",
            "professors",
            "students",
            "student_admissions"
        )
    ```

3. Configure your pipeline

    Still in dlt_pipeline.py, fill in the pipeline metadata:

    ```python
    pipeline = dlt.pipeline(
        pipeline_name="university_data",
        destination="duckdb",
        dataset_name="stg_university_data"
    )
    ```

4. Run the pipeline 

    Back in the terminal, run `python dlt_pipeline.py`

    This will create a DuckDB database called `university_data.duckdb`


Let's see what's in this database. Thankfully DuckDB offers a new handy UI to inspect the data in DuckDB.

In the terminal, type `duckdb -ui`

`SELECT * FROM stg_university_data.students;`

Duckdb contains the data extracted from Postgres!

## 🔁 Bonus: Experiment with Refresh and Incremental Loads

Once your initial pipeline is working, try exploring how dlt handles updates:
- Modify a row in Postgres and re-run the pipeline.
- Add a new row and re-run it again.
- Observe whether dlt refreshes the data or appends new rows.

You can configure dlt for full refresh or incremental loading based on your pipeline’s settings and primary keys. It also does data transformations and much more.

For more information, see dlt's documenation: https://dlthub.com/docs/intro

# 🧱 Data Modeling & Transformation

In this section, you’ll create a dimensional data model using the data we previously ingested into DuckDB from Postgres.

We’ll use a modeling pattern called ELT:
- Extract data from the source (Postgres)
- Load it into a staging layer (DuckDB)
- Transform it into an analytical model

## 🤷‍♂️ Why ELT?

Traditional ETL (Extract, Transform, Load) transforms data before it hits the data warehouse. But modern data pipelines use ELT, which lets you:
- Load raw data into your analytical engine first
- Transform data using scalable SQL logic
- Separate concerns by modeling data in clean, structured layers

We’ve already completed the “E” and “L” parts. Now we’re in the “T” phase—transforming the data into dimensional models for analytics and AI.

## 🛠️ Step-by-Step Instructions

1. Launch DuckDB CLI

    If you’re not already in DuckDB, start the CLI: `duckdb`

2. Create a Schema for the Serving Layer

    Create a new schema in DuckDB `CREATE SCHEMA serving;`

We just created a separate schema for serving the data. This is distinct from staging the data like we did in the prior section.

3. Next, let's create some tables. Open the file `duckdb_scripts/create_tables_ddb.sql`

- Copy all the SQL.
- Paste it into the DuckDB CLI and run it.

This script creates dimension and fact tables, such as:
- dim_students, dim_courses, dim_professors, dim_date
- fact_enrollments, fact_course_assignments

4. Populate the Star Schema

Now let’s populate the serving layer using the data from the staging schema:

`duckdb_scripts/migrate_postgres_to_duckdb_star_schema.sql`

- Open the file and copy all the SQL.
- Paste it into the DuckDB CLI.
- Run the script to transform and load the data.

You now have a functioning dimensional model in your serving schema!

## 🧪 Optional: Experiment with Updates & Incremental Loads

Once your model is working, try the following:
- Add new records in Postgres and rerun the pipeline.
- Update existing records and observe what happens when you rerun the transformation script.
- Explore how dlt handles refresh vs. incremental loading.

Because slowly changing dimensions are par for the course in data warehouse workshops, no need to rehash it for the millionth time.

## 🧹 Got an Error? Start Fresh

If something goes wrong during transformation, you can truncate the tables and try again.

TRUNCATE TABLE serving.fact_enrollments;
TRUNCATE TABLE serving.fact_course_assignments;

-- Then truncate dimension tables
TRUNCATE TABLE serving.dim_students;
TRUNCATE TABLE serving.dim_courses; 
TRUNCATE TABLE serving.dim_professors;
TRUNCATE TABLE serving.dim_date;

# 📊 Serving Data for Analytics & AI

From where I sit, data engineering is moving to the Serving layer of the data engineering lifecycle. The data warehouse is the cornerstone, but serving data from it evolves. This means the ability to create data and AI powered applications.

## 🖥️ Data-Powered Applications in Streamlit

Streamlit is an open-source Python library for building custom web apps for machine learning and data science. It’s perfect for quickly turning data scripts into interactive dashboards and apps—with just a few lines of Python.

Streamlit lets you:
- Display tables, charts, and metrics.
- Create interactive widgets (sliders, dropdowns, text inputs).
- Build full analytics dashboards or internal data tools.

## 🚀 Run Your First Streamlit App

Let's start your first Streamlit app to make sure things are running.

From your terminal in the project directory, type: `streamlit run streamlit_app/hello_world.py`

A browser window should open at `http://localhost:8501` showing a basic “Hello, Streamlit” app.

✅ If you see it—congrats! Your Streamlit environment is up and running.

Explore the app interface, including the dropdown menu in the top right.

## 🧪 Learn the Basics of Streamlit

Let’s go beyond “Hello World” and explore what Streamlit can do.

1. Open the file `streamlit_app/basics.py`

From your terminal in the project directory, type: `streamlit run streamlit_app/basics.py`

2.	Walk through the exercises inside the file. They demonstrate how to use common Streamlit features like displaying data, adding interactivity, and more.

The solutions to these exercises are located at `streamlit_app/basics_solutions.py`

Now that you've got a good grasp of Streamlit basics, let's connect our streamlit application to our data warehouse.

## 📈 Connect Streamlit to Your Data Warehouse

Here, we're going to look at more complex queries and data applications in our data warehouse.v

Now let’s build a more advanced app that interacts with your modeled data in DuckDB.
	1.	Stop the current app (Ctrl + C)

Let’s begin with a simple ranking. This query will show the five courses with the highest number of student enrollments.

```
SELECT c.course_title, COUNT(*) AS student_count
FROM fact_enrollments f
JOIN dim_courses c ON f.course_sk = c.course_sk
WHERE c.course_title = 'Intro to Computer Science'
GROUP BY c.course_title;
```

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



