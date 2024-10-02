pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = 'roicy/socialaws'
        IMAGE_TAG = 'latest'
        DOCKER_CREDENTIALS_ID = 'dockerhub_credentials' // Setup in Jenkins
    }
    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/roicy123/Socials.git', credentialsId: 'git_id'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${IMAGE_TAG}")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['ec2-ssh-key']) {
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@<EC2_IP> "docker pull ${DOCKER_HUB_REPO}:${IMAGE_TAG} && docker-compose down && docker-compose up -d"'
                }
            }
        }
    }
}
