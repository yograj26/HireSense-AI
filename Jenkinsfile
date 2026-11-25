pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Python Environment') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
            }
        }

        stage('Install CI Dependencies') {
            steps {
                sh '''
                    set -eu
                    .venv/bin/python -m pip install \
                        --disable-pip-version-check \
                        --retries 3 \
                        --timeout 120 \
                        -r requirements-ci.txt
                '''
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