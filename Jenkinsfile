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

                    grep -Eiv '^(torch|sentence[-_]transformers|transformers|tokenizers|huggingface[-_]hub|safetensors|hf[-_]xet|nvidia[-_]|cuda[-_]|triton)([<=>!~].*)?$' requirements.txt > requirements-ci.txt

                    echo "Installing lightweight CI dependencies..."
                    .venv/bin/python -m pip install --retries 3 --timeout 120 -r requirements-ci.txt pytest
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