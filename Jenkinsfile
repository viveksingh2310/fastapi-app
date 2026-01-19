pipeline {
    agent any

    environment {
        IMAGE_NAME = "vivek0231234/fastapi-app"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        DOCKER_CREDS = credentials('dockerhub-creds')
    }

    stages {

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Login to Docker Hub') {
            steps {
                bat """
                echo %DOCKER_CREDS_PSW% | docker login ^
                -u %DOCKER_CREDS_USR% --password-stdin
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                bat """
                docker push %IMAGE_NAME%:%IMAGE_TAG%
                docker tag %IMAGE_NAME%:%IMAGE_TAG% %IMAGE_NAME%:latest
                docker push %IMAGE_NAME%:latest
                """
            }
        }

        stage('Cleanup Old Docker Images') {
            steps {
                bat """
                docker image prune -f
                for /f "tokens=1,2" %%i in ('docker images %IMAGE_NAME% --format "{{.ID}} {{.Tag}}" ^| findstr /v latest') do docker rmi -f %%i
                """
            }
        }
    }

    post {
        always {
            bat "docker logout"
        }
    }
}