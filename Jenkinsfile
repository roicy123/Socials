pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = 'roicy/socialaws'
        IMAGE_TAG = 'latest'
        DOCKER_CREDENTIALS_ID = 'dockerhub_credentials' // Credentials setup in Jenkins
        EC2_IP = '54.165.88.63' // Replace with actual EC2 IP
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/roicy123/Socials.git', credentialsId: 'git_id'
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
                script {
                    sshagent (credentials: ['ec2-ssh-key']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} << 'EOF'
                            # Ensure Docker and Docker Compose are installed
                            sudo systemctl start docker || sudo apt-get install -y docker.io
                            sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                            sudo chmod +x /usr/local/bin/docker-compose
                            
                            # Check Docker and Docker Compose installation
                            docker --version
                            docker-compose --version
                            
                            # Pull the latest Docker image
                            docker pull ${DOCKER_HUB_REPO}:${IMAGE_TAG}
                            
                            # Stop any running containers and remove them
                            docker-compose down || echo "No containers to stop"
                            
                            # Start the application using Docker Compose
                            docker-compose up -d
                        EOF
                        """
                    }
                }
            }
        }
    }
}
