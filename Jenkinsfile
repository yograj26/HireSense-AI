pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Starting HireSense pipeline'
            }
        }

        stage('Python Environment') {
            steps {
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest tests -v'
            }
        }

        stage('Compile Python') {
            steps {
                bat 'python -m compileall app'
            }
        }
    }

    post {
        success {
            echo 'HireSense pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check test logs.'
        }
    }
}