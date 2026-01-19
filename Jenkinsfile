pipeline {
    agent any

    environment {
        IMAGE_NAME = "vivek0231234/demo-app"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        DOCKER_CREDS = credentials('dockerhub-creds')
    }

    stages {

        stage('Docker Login') {
            steps {
                bat """
                echo %DOCKER_CREDS_PSW% | docker login ^
                -u %DOCKER_CREDS_USR% --password-stdin
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Push Image') {
            steps {
                bat """
                docker push %IMAGE_NAME%:%IMAGE_TAG%
                docker tag %IMAGE_NAME%:%IMAGE_TAG% %IMAGE_NAME%:latest
                docker push %IMAGE_NAME%:latest
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
