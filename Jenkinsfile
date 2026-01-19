pipeline {
    agent any

    environment {
        IMAGE_NAME = "vivek0231234/fastapi-app"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        DOCKER_CREDS = credentials('dockerhub-creds')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/viveksingh2310/fastapi-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                """
            }
        }

        stage('Login to Docker Hub') {
            steps {
                sh """
                echo $DOCKER_CREDS_PSW | docker login \
                    -u $DOCKER_CREDS_USR --password-stdin
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                docker push $IMAGE_NAME:$IMAGE_TAG
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                docker push $IMAGE_NAME:latest
                """
            }
        }

        stage('Cleanup Old Docker Images') {
            when {
                success()
            }
            steps {
                sh """
                echo "Removing dangling images..."
                docker image prune -f

                echo "Removing old builds (except latest)..."
                docker images $IMAGE_NAME --format "{{.ID}} {{.Tag}}" | \
                grep -v latest | awk '{print $1}' | xargs -r docker rmi -f
                """
            }
        }
    }

    post {
        always {
            sh "docker logout"
        }
    }
}
