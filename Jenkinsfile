pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'social_media_feed.settings'
        PYTHONPATH = "/usr/src/app"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/roicy123/Socials.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def app = docker.build("socialaws")
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image("socialaws").inside {
                        sh 'pytest --ds=social_media_feed.settings' // Ensure it runs with Django settings
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    docker.image("socialaws").run("-d -p 8000:8000") // Deploy app in detached mode
                }
            }
        }
    }
}
