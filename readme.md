
### Contextualização para QA
Airflow é uma ferramenta de orquestração de tarefas. Em vez de testarmos apenas funcionalidades, podemos querer validar fluxos de dados, execução de jobs ou até automatizar testes em pipelines.”

### O que é uma DAG?
Uma DAG (Directed Acyclic Graph) é um grafo direcionado sem ciclos.
No contexto do Airflow, ela define uma sequência de tarefas com dependências bem definidas.
Ideal para orquestrar pipelines de dados, execuções automatizadas e até testes end-to-end em processos

### Estrutura de uma DAG:

```
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Definição da DAG
dag = DAG(
    'primeira_dag',
    description="Nossa primeira DAG",
    schedule_interval=None,  # Não executa automaticamente
    start_date=datetime(2025, 4, 10),
    catchup=False            # Evita execuções retroativas
)

# Tarefas da DAG
task1 = BashOperator(task_id="tks1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tks2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="tks3", bash_command="sleep 5", dag=dag)

# Definição da ordem de execução
task1 >> task2 >> task3
```

### Ordem de Execução

| Forma             | Código                    | Significado                      |
| ----------------- | ------------------------- | -------------------------------- |
| Sequencial        | `task1 >> task2 >> task3` | Executa uma após a outra         |
| Paralelismo       | `task1 >> [task2, task3]` | task2 e task3 rodam em paralelo  |
| Precedência comum | `[task1, task2] >> task3` | task3 só roda após task1 e task2 |


### Dica
dag=dag é opcional no with

```
with DAG(...) as dag:
    ...
```
Todas as tasks dentro do bloco já são vinculadas à DAG automaticamente.
Ou seja: não precisa passar dag=dag nas tasks.

| Fora do `with`                      | Dentro do `with`           |
| ----------------------------------- | -------------------------- |
| `task = BashOperator(..., dag=dag)` | `task = BashOperator(...)` |


### set_upstream e set_downstream (menos comum, mas útil)
Formas alternativas ao >> e << para definir dependência entre tarefas.
Úteis em loops, listas ou geração dinâmica de DAGs.

Exemplos
````
task2.set_upstream(task1)     # task1 >> task2  
task1.set_downstream(task2)   # task1 >> task2
````
Direções:
- set_upstream(task) → esta task depende de task
- set_downstream(task) → esta task vem antes de task


```
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
```

### Principais operadores
| Operador                             | O que faz                                      | Exemplo de uso                          |
| ------------------------------------ | ---------------------------------------------- | --------------------------------------- |
| `BashOperator`                       | Executa comandos no terminal/shell             | Rodar scripts, comandos `pytest`, etc.  |
| `PythonOperator`                     | Executa uma função Python                      | Validar dados, chamar testes unitários  |
| `BranchPythonOperator`               | Desvia o fluxo da DAG com base em uma condição | Fluxo A ou B dependendo de um teste     |
| `DummyOperator` (ou `EmptyOperator`) | Usado como placeholder ou marcador             | Agrupar etapas, teste de estrutura      |
| `TriggerDagRunOperator`              | Dispara outra DAG                              | Orquestrar múltiplas DAGs               |
| `EmailOperator`                      | Envia e-mails                                  | Alertas de erro ou sucesso              |
| `Sensor` (ex: `FileSensor`)          | Espera um evento ou arquivo                    | Aguardar chegada de arquivo para testes |
| `SQLExecuteQueryOperator`            | Executa comandos SQL no banco                  | Validar contagem de registros, status, etc. |


#### Para times de QA, destaque:
- PythonOperator: rodar funções de teste automatizado
- BashOperator: executar comandos como pytest, robot, curl, etc.
- BranchPythonOperator: criar lógica condicional em testes
- Sensor: aguardar evento (útil em testes de integração)


### O que são Trigger Rules?
Trigger rules definem a condição para uma task ser executada, com base no resultado das tarefas que vêm antes dela.

Por padrão, uma task só roda se todas as anteriores tiverem sucesso.

| Trigger Rule             | Quando a task roda                                  | Exemplo de uso                                |
| ------------------------ | --------------------------------------------------- | --------------------------------------------- |
| `all_success` *(padrão)* | Todas as upstreams têm que ter sucesso (`success`)  | Execução normal de etapas sequenciais         |
| `all_failed`             | Todas as anteriores falharam                        | Mandar alerta se tudo falhar                  |
| `one_success`            | Pelo menos uma upstream teve sucesso                | Continuar o fluxo mesmo com falhas parciais   |
| `one_failed`             | Pelo menos uma upstream falhou                      | Tarefa de correção ou notificação de erro     |
| `none_failed`            | Nenhuma falhou (mesmo que algumas estejam skipadas) | Situação tolerante a `skips`, mas não a erros |
| `none_skipped`           | Nenhuma task foi pulada                             | Garantir execução total                       |
| `always`                 | Roda **independente** do status das anteriores      | Tarefa de limpeza ou log final                |

#### Em QA, para que usar?
- always: limpar ambiente de testes, mesmo após falha
- one_failed: mandar e-mail se qualquer etapa do teste falhar
- none_skipped: garantir que um grupo de testes tenha sido executado
- one_success: considerar o teste válido se pelo menos uma estratégia passou

Exemplos:

A task3 só vai rodar se pelo menos uma das anteriores (task1 ou task2) falhar.
Uso comum em QA: disparar uma notificação ou log de erro parcial.

```
dag = DAG('trigger_1', description="Trigger 1",
          schedule_interval=None, start_date=datetime(2025,4,10),
          catchup=False)

task1 = BashOperator(task_id="tks1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tks2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="tks3", bash_command="sleep 5", dag=dag, trigger_rule='one_failed')

[task1,task2] >> task3
```

Aqui, a task1 sempre falha (exit 1), então a task3 vai rodar porque a regra é "one_failed".
Ideal para simular comportamento de tarefas em cenários com falhas controladas.
```
dag = DAG('trigger_2', description="Trigger 2",
          schedule_interval=None, start_date=datetime(2025,4,10),
          catchup=False)

task1 = BashOperator(task_id="tks1", bash_command="exit 1", dag=dag)
task2 = BashOperator(task_id="tks2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="tks3", bash_command="sleep 5", dag=dag, trigger_rule='one_failed')

[task1,task2] >> task3
```

A task3 só será executada se todas as anteriores falharem. Como task1 e task2 têm exit 1, elas vão falhar — e task3 vai rodar.
Uso em QA: executar ação de fallback apenas se tudo deu errado.
```
dag = DAG('trigger_3', description="Trigger 3",
          schedule_interval=None, start_date=datetime(2025,4,10),
          catchup=False)

task1 = BashOperator(task_id="tks1", bash_command="exit 1", dag=dag)
task2 = BashOperator(task_id="tks2", bash_command="exit 1", dag=dag)
task3 = BashOperator(task_id="tks3", bash_command="sleep 5", dag=dag, trigger_rule='all_failed')

[task1,task2] >> task3
```


### Envio de E-mails com EmailOperator
Permite enviar e-mails automáticos a partir da DAG — útil para alertas, notificações de sucesso ou falha em pipelines de QA.

Exemplo de uso:
```

```


### Envio automático de e-mail por falha
Além de usar o EmailOperator, o Airflow permite enviar e-mails automaticamente quando uma task falha ou é reexecutada, sem precisar criar uma task de e-mail separada.

Isso é configurado nos parâmetros da DAG ou da task

```
default_args = {
    'owner': 'qa_team',
    'email': ['qa@empresa.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'dag_com_alerta',
    default_args=default_args,
    description='DAG com alerta por e-mail',
    schedule_interval=None,
    start_date=datetime(2025, 4, 10),
    catchup=False
)

```

#### O que esses parâmetros fazem:
| Parâmetro          | Significado                                             |
| ------------------ | ------------------------------------------------------- |
| `email`            | Lista de destinatários                                  |
| `email_on_failure` | Envia e-mail quando a task **falhar**                   |
| `email_on_retry`   | Envia e-mail a cada **tentativa de reexecução** da task |


##### Uso em QA:

- Receber notificação automática se um teste falhar
- Evitar excesso de e-mails em tentativas de reexecução (email_on_retry=False)
- Combinar com retries para monitorar instabilidades