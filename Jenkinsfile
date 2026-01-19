pipeline {
    agent any

    environment {
        IMAGE_NAME = 'vivek0231234/demo-app'
        IMAGE_TAG  = "${BUILD_NUMBER}"
        DOCKERHUB  = credentials('dockerhub-cred')
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
                bat "docker tag %IMAGE_NAME%:%IMAGE_TAG% %IMAGE_NAME%:latest"
            }
        }

        stage('Docker Login') {
            steps {
                bat '''
                echo %DOCKERHUB_PSW% | docker login -u %DOCKERHUB_USR% --password-stdin
                '''
            }
        }

        stage('Push Image') {
            steps {
                bat "docker push %IMAGE_NAME%:%IMAGE_TAG%"
                bat "docker push %IMAGE_NAME%:latest"
            }
        }
    }

    post {
        success {
            bat '''
            docker image prune -f
            docker images vivek0231234/demo-app -q | more +1 | for %%i in (%%~n) do docker rmi -f %%i
            '''
        }
    }
}
