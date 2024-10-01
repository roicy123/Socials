pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/roicy123/Socials.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def app = docker.build("socials")
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image("socials").inside {
                        sh 'pytest' // Use your testing command
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    docker.image("socials").run("-d -p 8000:8000") // Run your app in detached mode
                }
            }
        }
    }
}
