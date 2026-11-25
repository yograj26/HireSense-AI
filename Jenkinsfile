pipeline {
    agent any

    stages {
        stage('Python Environment') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '.venv/bin/python -m pip install --upgrade pip'
                sh '.venv/bin/python -m pip install -r requirements.txt pytest'
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m pytest tests -v'
            }
        }

        stage('Compile Application') {
            steps {
                sh '.venv/bin/python -m compileall app'
            }
        }

        stage('Git Validation') {
            steps {
                sh 'git diff --check'
            }
        }
    }

    post {
        success {
            echo 'HireSense AI CI Pipeline Passed!'
        }
        failure {
            echo 'Build failed. Check Console Output.'
        }
    }
}