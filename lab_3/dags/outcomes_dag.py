from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
from etl_scripts.transform import transform_data
from etl_scripts.load import load_data, load_fact_data

SOURCE_API = "https://data.austintexas.gov/resource/9t4d-g238.json"
SOURCE_URL = "https://data.austintexas.gov/api/views/9t4d-g238/rows.csv"
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')
CSV_TARGET_DIR = AIRFLOW_HOME + '/data/{{ ds }}/downloads'
CSV_TARGET_FILE = CSV_TARGET_DIR +'/outcomes_{{ ds }}.csv'

PQ_TARGET_DIR = AIRFLOW_HOME + '/data/{{ ds }}/processed'
with DAG(
    dag_id ="outcomes_dag",
    start_date = datetime(2023,11,1),
    schedule_interval = '@daily'

) as dag:
    extract = BashOperator(
        task_id="extract",
        bash_command=f"curl --create-dirs -o {CSV_TARGET_FILE} {SOURCE_API}",
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable= transform_data,
        op_kwargs = {
            'source_csv': CSV_TARGET_FILE,
            'target_dir': PQ_TARGET_DIR
        }
    )

    transform_api = PythonOperator(
        task_id="transform_api",
        python_callable= fetch_data_and_save_csv,
        op_kwargs = {
            'api_url': CSV_TARGET_FILE,
            'csv_file_path': PQ_TARGET_DIR
        }
    )

    load_animal_dim = PythonOperator(
        task_id="load_animal_dim",
        python_callable= load_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR+'/dim_animal.parquet',
            'table_name':'dim_animal',
            'key': 'animal_id'
        }
    )

    load_dates_dim = PythonOperator(
        task_id="load_dates_dim",
        python_callable= load_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR+'/dim_dates.parquet',
            'table_name':'dim_dates',
            'key': 'date_id'
        }
    )

    load_outcome_types_dim = PythonOperator(
        task_id="load_outcome_types_dim",
        python_callable= load_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR+'/dim_outcome_types.parquet',
            'table_name':'dim_outcome_types',
            'key': 'outcome_type_id'
        }
    )

    load_outcomes_fct = PythonOperator(
        task_id="load_outcomes_fct",
        python_callable= load_fact_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR+'/fct_outcomes.parquet',
            'table_name':'fct_outcomes',
        }
    )
    extract >> transform >> [load_animal_dim,load_dates_dim, load_outcome_types_dim] >> load_outcomes_fct