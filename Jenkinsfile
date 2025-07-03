pipeline {
    agent any

    stages {
        stage('Clonar código') {
            steps {
                git url: 'https://github.com/Jheymisson/airflow-poc.git', branch: 'master'
            }
        }

        stage('Executar testes') {
            steps {
                sh '''
                    docker-compose exec -T airflow-webserver bash -c "
                        pip install -q pytest &&
                        pytest /opt/airflow/tests/test_dags_geral.py
                    "
                '''
            }
        }

        stage('Deploy') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                echo 'Testes passaram, executando deploy do Airflow'
                sh 'docker-compose up -d --build'
            }
        }
    }

    post {
        failure {
            echo 'Build falhou. Verifique os testes.'
        }
    }
}
