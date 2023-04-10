pipeline {
    agent any

    stages {
        // docker Deploy
        stage('Deploy Docker') {
          agent any
          steps {
            echo 'Deploy Docker '
            sh 'docker compose docker-compose.yml up -d'
          }
          post {
            failure {
              error 'This pipeline stops here...'
            }
          }
        }
    }
}