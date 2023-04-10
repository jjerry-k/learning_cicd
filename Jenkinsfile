pipeline {
    agent any

    stages {
        // docker Deploy
        stage("Deploy app") {
          agent any
          steps {
            echo "Deploy using Docker"
            sh "docker compose up -d"
          }
          post {
            failure {
              error "This pipeline stops here..."
            }
          }
        }
    }
}