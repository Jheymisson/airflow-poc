# Importa o pytest para os testes e o DagBag que é o container das DAGs do Airflow
import pytest
from airflow.models import DagBag

# Carrega todas as DAGs disponíveis no diretório configurado do Airflow
dag_bag = DagBag()

# Testa se todas as DAGs foram carregadas sem erros de importação
def test_dags_importadas_sem_erro():
    # Se alguma DAG tiver erro de import, o teste falha
    assert len(dag_bag.import_errors) == 0, f"Erros ao importar DAGs: {dag_bag.import_errors}"

# Teste parametrizado para verificar se cada DAG tem o número esperado de tasks
@pytest.mark.parametrize("dag_id, num_tasks", [
    ('1_basica_dag', 3),
    ('2_basica_dag', 3),
    ('3_basica_dag', 3),
    ('4_basica_dag', 3),
    ('trigger_1', 3),
    ('trigger_2', 3),
    ('trigger_3', 3),
    ('trigger_4', 9),
    ('email_test', 7),
])
def test_dags_tem_numero_esperado_de_tasks(dag_id, num_tasks):
    # Recupera a DAG pelo ID
    dag = dag_bag.get_dag(dag_id)
    # Verifica se a DAG foi encontrada
    assert dag is not None, f"DAG {dag_id} não encontrada"
    # Verifica se a DAG tem a quantidade de tasks esperada
    assert len(dag.tasks) == num_tasks, f"DAG {dag_id} deveria ter {num_tasks} tasks, mas tem {len(dag.tasks)}"

# Testa se a task 'send_email' da DAG 'email_test' tem o trigger_rule esperado
def test_send_email_trigger_rule():
    # Recupera a DAG
    dag = dag_bag.get_dag('email_test')
    # Recupera a task específica da DAG
    task = dag.get_task('send_email')
    # Verifica se o trigger_rule da task está configurado como 'one_failed'
    assert task.trigger_rule == 'one_failed'
