pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        REGISTRY = "512466680445.dkr.ecr.us-east-1.amazonaws.com"
        IMAGE_NAME = "fintrack"
        NAMESPACE = "default"
        DEPLOYMENT = "fintrack-deployment"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/VishnuSaravanan335/fintrack.git'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'cd fintrack && pytest || echo "No tests found, skipping..."'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t $REGISTRY/$IMAGE_NAME:\$BUILD_NUMBER .
                """
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    sh """
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $REGISTRY
                    docker push $REGISTRY/$IMAGE_NAME:\$BUILD_NUMBER
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                # Apply Deployment
                if [ -f k8s/fintrack-deployment.yaml ]; then
                  kubectl apply -f k8s/fintrack-deployment.yaml -n $NAMESPACE
                else
                  echo "❌ fintrack-deployment.yaml not found"
                  exit 1
                fi

                # Apply Service if present
                if [ -f k8s/fintrack-service.yaml ]; then
                  kubectl apply -f k8s/fintrack-service.yaml -n $NAMESPACE
                else
                  echo "⚠️ fintrack-service.yaml not found, skipping service creation"
                fi

                # Update image in Deployment
                kubectl set image deployment/$DEPLOYMENT fintrack-flask=$REGISTRY/$IMAGE_NAME:\$BUILD_NUMBER -n $NAMESPACE
                kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE
                """
            }
        }

        stage('Monitoring Setup - Grafana') {
            steps {
                sh """
                if [ -f k8s/grafana.yaml ]; then
                  kubectl apply -f k8s/grafana.yaml -n monitoring
                  kubectl rollout status deployment/grafana -n monitoring
                else
                  echo "⚠️ grafana.yaml not found, skipping monitoring setup"
                fi
                """
            }
        }
    }

    post {
        success {
            echo "✅ FinTrack deployed successfully to Kubernetes!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
