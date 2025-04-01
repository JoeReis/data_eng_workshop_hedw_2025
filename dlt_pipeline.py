import dlt
from dlt.sources.sql_database import sql_database

def load_university_pipeline():
    source = sql_database().with_resources("courses", "course_assignments", "enrollments", "professors", "students", "student_admissions")
    
    # source.professors.apply_hints(incremental=dlt.sources.incremental("created_at")) #incremental load
    
    pipeline = dlt.pipeline(
        pipeline_name="university_data", #duckdb database name
        destination='duckdb',
        dataset_name="stg_university_data", #staging zone
    )
    
    load_info = pipeline.run(source)
    
    print(load_info)
    
if __name__ == "__main__":
    load_university_pipeline()