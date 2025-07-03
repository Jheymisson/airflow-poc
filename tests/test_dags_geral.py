
import pytest
from airflow.models import DagBag

dag_bag = DagBag()

def test_dags_importadas_sem_erro():
    assert len(dag_bag.import_errors) == 0, f"Erros ao importar DAGs: {dag_bag.import_errors}"

@pytest.mark.parametrize("dag_id, num_tasks", [
    ('primeira_dag', 3),
    ('segunda_dag', 3),
    ('terceira_dag', 3),
    ('quarta_dag', 3),
    ('trigger_1', 3),
    ('trigger_2', 3),
    ('trigger_3', 3),
    ('trigger_4_complexa', 9),
    ('email_test', 7),
])
def test_dags_tem_numero_esperado_de_tasks(dag_id, num_tasks):
    dag = dag_bag.get_dag(dag_id)
    assert dag is not None, f"DAG {dag_id} não encontrada"
    assert len(dag.tasks) == num_tasks, f"DAG {dag_id} deveria ter {num_tasks} tasks, mas tem {len(dag.tasks)}"

def test_send_email_trigger_rule():
    dag = dag_bag.get_dag('email_test')
    task = dag.get_task('send_email')
    assert task.trigger_rule == 'one_failed'
