pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'social_media_feed.settings'
        PYTHONPATH = "/usr/src/app"
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t socialaws:latest .'  // Build Docker image
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag socialaws:latest roicy/socialaws:latest'  // Tag the image
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Using the Docker access token for authentication
                    withCredentials([string(credentialsId: 'dockertoken', variable: 'DOCKER_TOKEN')]) {
                        sh '''
                        echo "$DOCKER_TOKEN" | docker login -u roicy --password-stdin
                        docker push roicy/socialaws:latest
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("roicy/socialaws:latest").inside {
                        sh 'pytest --ds=social_media_feed.settings'  // Run tests with Django settings
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'gemini-api-key', variable: 'GEMINI_API_KEY')]) {
                        sshagent (credentials: ['my-ec2-key']) {
                            sh '''
                            ssh -o StrictHostKeyChecking=no ubuntu@54.165.88.63 << 'EOF'
                            cd /var/lib/jenkins/workspace/textwave
                            # Stop the running containers
                            docker-compose down || true

                            # Pull the latest image from Docker Hub
                            docker pull roicy/socialaws:latest

                            # Create an .env file with the GEMINI_API_KEY
                            echo "GEMINI_API_KEY=$GEMINI_API_KEY" > .env

                            # Bring up the services with the latest image
                            docker-compose up -d
EOF
                            '''
                        }
                    }
                }
            }
        }
    }
}
