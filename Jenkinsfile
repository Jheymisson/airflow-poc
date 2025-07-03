pipeline {
    agent any

    stages {
        stage('Executar testes') {
            steps {
                dir('/Users/jheymissonalbuquerque/Documents/estudo_airflow') {
                {
                    sh '''
                        docker-compose exec -T airflow-webserver bash -c "
                          pip install -q pytest &&
                          pytest /opt/airflow/tests/test_dags_geral.py
                        "
                    '''
                }
            }
        }

        stage('Deploy') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                dir('caminho/do/seu/projeto') {
                    sh '''
                        docker-compose exec -T airflow-webserver bash -c "
                          airflow dags reload
                        "
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo 'Build falhou. Verifique os testes.'
        }
    }
}
