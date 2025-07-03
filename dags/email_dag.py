# DAG de exemplo com envio de e-mail em caso de falha de tarefa
# Referência: Curso Domine Apache Airflow - https://www.eia.ai/

from airflow import DAG
from airflow.operators.bash_operator import BashOperator  # Operador que executa comandos no bash
from airflow.operators.email_operator import EmailOperator  # Operador que envia e-mails
from datetime import datetime, timedelta

# Argumentos padrão aplicados a todas as tasks
default_args = {
    'depends_on_past': False,               # Task não depende de execuções anteriores
    'start_date': datetime(2023, 3, 5),     # Data inicial da DAG
    'email': ['aws@evoluth.com.br'],        # E-mail de notificação
    'email_on_failure': True,               # Envia e-mail em caso de falha
    'email_on_retry': False,                # Não envia e-mail em caso de tentativa de reexecução
    'retries': 1,                           # Número de tentativas
    'retry_delay': timedelta(seconds=10)    # Tempo de espera antes de uma nova tentativa
}

# Definição da DAG
dag = DAG(
    'email_test',
    description="Email",
    default_args=default_args,
    schedule_interval=None,                # A DAG não é agendada automaticamente
    catchup=False,                         # Não executa execuções passadas
    default_view='graph',                  # Visualização padrão no Airflow Web UI
    tags=['processo', 'tag', 'pipeline']   # Tags para facilitar a busca
)

# Tarefas simulando etapas de execução
task1 = BashOperator(task_id="tsk1", bash_command="sleep 1", dag=dag)
task2 = BashOperator(task_id="tsk2", bash_command="sleep 1", dag=dag)
task3 = BashOperator(task_id="tsk3", bash_command="sleep 1", dag=dag)

# Esta tarefa está programada para falhar (exit 1 = erro)
task4 = BashOperator(task_id="tsk4", bash_command="exit 1", dag=dag)

# Estas tarefas só serão executadas se nenhuma anterior falhar
task5 = BashOperator(task_id="tsk5", bash_command="sleep 1", dag=dag, trigger_rule='none_failed')
task6 = BashOperator(task_id="tsk6", bash_command="sleep 1", dag=dag, trigger_rule='none_failed')

# Tarefa de envio de e-mail, que será executada se **ao menos uma tarefa anterior falhar**
send_email = EmailOperator(
    task_id="send_email",
    to="aws@evoluth.com.br",                         # E-mail de destino
    subject="Airflow Error",                         # Assunto do e-mail
    html_content="""<h3>Ocorreu um erro na Dag. </h3>
                    <p>Dag: send_email </p>""",      # Corpo do e-mail (HTML)
    dag=dag,
    trigger_rule="one_failed"                        # Executa se qualquer tarefa anterior falhar
)

# Define a ordem das tarefas:
# task1 e task2 executam em paralelo → task3 → task4 (que falha)
[task1, task2] >> task3 >> task4

# task4 → [task5, task6, send_email]
# → task5 e task6 serão ignoradas porque task4 falha (trigger_rule='none_failed')
# → send_email será executado porque task4 falhou (trigger_rule='one_failed')
task4 >> [task5, task6, send_email]
