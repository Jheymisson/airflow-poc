from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Criação da DAG chamada "3_basica_dag"
dag = DAG('3_basica_dag', description="Nossa terceita dag",
          schedule_interval=None, start_date=datetime(2025, 4, 10),
          catchup=False)

# Define três tarefas que executam "sleep 5"
task1 = BashOperator(task_id="tks1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tks2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="tks3", bash_command="sleep 5", dag=dag)

# task1 e task2 rodam em paralelo, e ambas devem terminar antes de task3 iniciar
[task1, task2] >> task3
