
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Starting HireSense AI pipeline'
            }
        }

        stage('Python Check') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
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
    }

    post {
        success {
            echo 'HireSense AI pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}
