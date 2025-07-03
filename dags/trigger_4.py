from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG('trigger_4_complexa', description="Trigger 4",
          schedule_interval=None, start_date=datetime(2025,4,10),
          catchup=False)

task1 = BashOperator(task_id="tks1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tks2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="tks3", bash_command="sleep 5", dag=dag)
task4 = BashOperator(task_id="tks4", bash_command="sleep 5", dag=dag)
task5 = BashOperator(task_id="tks5", bash_command="sleep 5", dag=dag)
task6 = BashOperator(task_id="tks6", bash_command="sleep 5", dag=dag)
task7 = BashOperator(task_id="tks7", bash_command="sleep 5", dag=dag)
task8 = BashOperator(task_id="tks8", bash_command="sleep 5", dag=dag)
task9 = BashOperator(task_id="tks9", bash_command="sleep 5", dag=dag, trigger_rule='one_failed')

task1 >> task2
task3 >> task4
[task2, task4] >> task5 >> task6
task6 >> [task7, task8, task9]