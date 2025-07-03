from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG('trigger_1', description="Trigger 1",
          schedule_interval=None, start_date=datetime(2025,4,10),
          catchup=False)

task1 = BashOperator(task_id="tks1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tks2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="tks3", bash_command="sleep 5", dag=dag, trigger_rule='one_failed')

[task1,task2] >> task3