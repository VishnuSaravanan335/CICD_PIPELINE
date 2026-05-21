pipeline {
    agent any

    environment {
        REGISTRY = "your-dockerhub-username"
        IMAGE_NAME = "fintrack"
        NAMESPACE = "default"
        DEPLOYMENT = "fintrack-deployment"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/VishnuSaravanan335/fintrack.git'
            }
        }

        stage('Build & Setup') {
            steps {
                sh '''
                python3 -m venv venv
                ./venv/bin/pip install --upgrade pip
                ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh './venv/bin/python -m unittest discover -s tests'
            }
        }

        stage('Check Files') {
            steps {
                sh 'ls -al'
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    // Standard secure credentials lookup for docker login
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USER --password-stdin"
                        sh "docker build -t $REGISTRY/$IMAGE_NAME:\$BUILD_NUMBER -f Dockerfile ."
                        sh "docker push $REGISTRY/$IMAGE_NAME:\$BUILD_NUMBER"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Apply deployment resources first (in case it does not exist)
                    sh "kubectl apply -f k8s/deployment.yaml -n $NAMESPACE"
                    // Perform rolling update with the new image tag
                    sh "kubectl set image deployment/$DEPLOYMENT $IMAGE_NAME=$REGISTRY/$IMAGE_NAME:\$BUILD_NUMBER -n $NAMESPACE"
                    // Monitor rollout status
                    sh "kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE"
                }
            }
        }

        stage('Monitoring Setup') {
            steps {
                script {
                    // Deploy monitoring manifests (Prometheus & Grafana)
                    sh """
                    kubectl apply -f k8s/prometheus.yaml -n monitoring
                    kubectl apply -f k8s/grafana.yaml -n monitoring
                    """
                }
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
