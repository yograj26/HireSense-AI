pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Starting HireSense AI CI Pipeline'
                checkout scm
            }
        }

        stage('Python Environment') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests -v'
            }
        }

        stage('Compile Application') {
            steps {
                sh 'python3 -m compileall app'
            }
        }
    }

    post {
        success {
            echo 'HireSense AI pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}