pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Version') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest tests -v'
            }
        }

        stage('Compile Application') {
            steps {
                bat 'python -m compileall app'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t hiresense-ai .'
            }
        }
    }

    post {
        success {
            echo 'HireSense AI CI pipeline passed successfully!'
        }

        failure {
            echo 'Pipeline failed. Review the stage logs.'
        }
    }
}