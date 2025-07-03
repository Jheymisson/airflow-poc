from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG('quarta_dag', description="Nossa quarta dag",
          schedule_interval=None, start_date=datetime(2025,4,10),
          catchup=False) as dag:

    task1 = BashOperator(task_id="tks1", bash_command="sleep 5")
    task2 = BashOperator(task_id="tks2", bash_command="sleep 5")
    task3 = BashOperator(task_id="tks3", bash_command="sleep 5")

    task1.set_upstream(task2)
    task2.set_upstream(task3)