# Importa a classe DAG, que é usada para criar um pipeline de tarefas no Airflow
from airflow import DAG

# Importa o operador BashOperator, que permite executar comandos de terminal (bash)
from airflow.operators.bash_operator import BashOperator

# Importa a função datetime para definir a data de início da DAG
from datetime import datetime

# Cria uma DAG chamada "1_basica_dag"
# - description: texto que descreve o propósito da DAG
# - schedule_interval=None: significa que ela não será executada automaticamente (somente manual)
# - start_date: define quando a DAG pode começar a rodar
# - catchup=False: não executa datas passadas (evita múltiplas execuções atrasadas)
dag = DAG('1_basica_dag', description="Nossa primeira dag",
          schedule_interval=None, start_date=datetime(2025, 4, 10),
          catchup=False)

# Define a primeira tarefa da DAG, que executa o comando 'sleep 5' no terminal (espera 5 segundos)
task1 = BashOperator(
    task_id="tks1",                  # Nome identificador da tarefa
    bash_command="sleep 5",         # Comando que será executado
    dag=dag                          # Referência à DAG onde a task será usada
)

# Segunda tarefa com o mesmo comando
task2 = BashOperator(
    task_id="tks2",
    bash_command="sleep 5",
    dag=dag
)

# Terceira tarefa com o mesmo comando
task3 = BashOperator(
    task_id="tks3",
    bash_command="sleep 5",
    dag=dag
)

# Define a ordem de execução:
# - task1 será executada primeiro
# - depois task2
# - por fim task3
task1 >> task2 >> task3
