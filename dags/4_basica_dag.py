from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Usa o bloco "with" para criar a DAG, facilitando a leitura e escopo
with DAG('4_basica_dag', description="Nossa quarta dag",
          schedule_interval=None, start_date=datetime(2025, 4, 10),
          catchup=False) as dag:

    # Define as tarefas que executam "sleep 5"
    task1 = BashOperator(task_id="tks1", bash_command="sleep 5")
    task2 = BashOperator(task_id="tks2", bash_command="sleep 5")
    task3 = BashOperator(task_id="tks3", bash_command="sleep 5")

    # Define a ordem de execução manualmente:
    # task3 → task2 → task1 (repare que é de "baixo para cima")
    task1.set_upstream(task2)  # task1 depende da finalização de task2
    task2.set_upstream(task3)  # task2 depende da finalização de task3
