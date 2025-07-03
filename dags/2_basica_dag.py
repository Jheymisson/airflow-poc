# Importa a classe DAG para criar o fluxo de tarefas
from airflow import DAG

# Importa o BashOperator para executar comandos de terminal
from airflow.operators.bash_operator import BashOperator

# Importa datetime para definir a data inicial
from datetime import datetime

# Criação da DAG chamada "2_basica_dag"
dag = DAG('2_basica_dag', description="Nossa segunda dag",
          schedule_interval=None, start_date=datetime(2025, 4, 10),
          catchup=False)

# Define três tarefas que executam "sleep 5"
task1 = BashOperator(task_id="tks1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tks2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="tks3", bash_command="sleep 5", dag=dag)

# task1 é executada primeiro, depois task2 e task3 rodam em paralelo
task1 >> [task2, task3]
