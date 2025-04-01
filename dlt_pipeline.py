import sys
import dlt
from dlt.sources.sql_database import sql_database
from dlt.sources.incremental import incremental

def load_university_pipeline(use_incremental=False):
    source = sql_database().with_resources(
        "courses", "course_assignments", "enrollments", 
        "professors", "students", "student_admissions"
    )
    
    if use_incremental:
        source.students.apply_hints(incremental=incremental("created_at"))
    
    pipeline = dlt.pipeline(
        pipeline_name="university_data",
        destination="duckdb",
        dataset_name="stg_university_data",
    )
    
    load_info = pipeline.run(source)
    print(load_info)

if __name__ == "__main__":
    incremental_flag = "--incremental" in sys.argv
    load_university_pipeline(use_incremental=incremental_flag)