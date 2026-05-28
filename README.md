# 📈 FinTrack: End-to-End GitOps CI/CD Pipeline

[![Python Version](https://img.shields.io/badge/Python-3.11-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Flask Framework](https://img.shields.io/badge/Flask-3.0-lightgrey.svg?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Dockerized](https://img.shields.io/badge/Docker-Enabled-blue.svg?style=flat-square&logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-blue.svg?style=flat-square&logo=kubernetes)](https://kubernetes.io/)
[![AWS Integration](https://img.shields.io/badge/AWS-ECR-orange.svg?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/)
[![CI/CD Pipeline](https://img.shields.io/badge/Jenkins-Declarative-red.svg?style=flat-square&logo=jenkins)](https://www.jenkins.io/)

**FinTrack** is an enterprise-grade personal finance tracking web application developed using **Python Flask** and structured around a high-performance **GitOps CI/CD delivery pipeline**. 

This repository serves as a reference implementation for a modern containerized application lifecycle. It automates testing, builds immutable Docker images, publishes artifacts to Amazon ECR, deploys multi-replica pods to a Kubernetes cluster, and actively monitors system health using Prometheus and Grafana.

---

## 🗺️ System & CI/CD Flow Diagram

The dynamic flowchart below displays the automated lifecycle of a code modification, starting from a local Git commit to live deployment and instrumentation:

```mermaid
flowchart TD
    %% Define Nodes
    Dev([💻 Developer Workspace])
    GitHub[🌐 GitHub Repository]
    Jenkins[⚙️ Jenkins Automation Server]
    
    subgraph Testing & Packaging
        Pytest[🧪 Pytest Suite]
        DockerBuild[🐳 Docker Build]
    end

    subgraph AWS Cloud Infrastructure
        ECR[📦 AWS ECR Registry]
    end

    subgraph EKS / Kubernetes Cluster
        K8sDeploy[☸️ FinTrack Deployment <br/> 2 Replicas]
        K8sSvc[🔌 FinTrack Service <br/> LoadBalancer]
    end

    subgraph Observability Stack
        Prom[🔥 Prometheus Server]
        Grafana[📊 Grafana Dashboards]
    end

    %% Flows
    Dev -->|1. git push| GitHub
    GitHub -->|2. Webhook Trigger| Jenkins
    Jenkins -->|3. Clone & Test| Pytest
    Pytest -->|Pass| DockerBuild
    DockerBuild -->|4. Authenticate & Push| ECR
    ECR -->|5. Apply Manifests| K8sDeploy
    K8sDeploy -->|6. Expose Service| K8sSvc
    K8sSvc -->|7. Scraping Metrics| Prom
    Prom -->|8. Visualizes Data| Grafana

    %% Styling
    classDef main fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef action fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#34d399;
    classDef cloud fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#fbbf24;
    classDef k8s fill:#0f172a,stroke:#06b6d4,stroke-width:2px,color:#22d3ee;
    classDef monitor fill:#0f172a,stroke:#ec4899,stroke-width:2px,color:#f472b6;

    class Dev,GitHub,Jenkins main;
    class Pytest,DockerBuild action;
    class ECR cloud;
    class K8sDeploy,K8sSvc k8s;
    class Prom,Grafana monitor;
```

---

## 🏗️ Technical Architecture Deep-Dive

FinTrack is engineered around a clean, scalable architectural pattern:

### 1. Application Layer (MVC Pattern)
*   **Flask Blueprints:** Application routes are divided into isolated logical sub-modules ([auth.py](file:///w:/fintrack/fintrack/routes/auth.py), [dashboard.py](file:///w:/fintrack/fintrack/routes/dashboard.py), [expense.py](file:///w:/fintrack/fintrack/routes/expense.py), and [income.py](file:///w:/fintrack/fintrack/routes/income.py)) to ensure ease of testing.
*   **Extensions & Security:** Utilizes `flask-bcrypt` for cryptographic password hashing, `flask-login` for secure user sessions, and `flask-wtf` to guard against CSRF vulnerabilities.

### 2. Database Layer
*   **SQLAlchemy ORM:** Encapsulates database models for object-relational mapping, letting you transition between SQLite (local development) and PostgreSQL/MySQL (production RDS environments) via simple environment configurations.

### 3. Containerization & Isolation
*   **Docker Container:** Leverages a lightweight `python:3.11-slim` base image to optimize layer sizes, minimize security vulnerabilities, and run isolated sandboxes.

### 4. GitOps CI/CD Orchestration
*   **Jenkins Pipeline:** A declarative pipeline automating code pulls, static code tests using `pytest`, ECR authentication, and rolling updates to Kubernetes clusters.

### 5. Observability & Monitoring
*   **Prometheus & Grafana:** Dedicated namespaces scrape metrics from application pods. PromQL charts monitor server errors, response times, memory use, and CPU utilization.

---

## 📂 Repository Structure

```text
fintrack/
├── Dockerfile                      # Multistage-ready Python Dockerfile
├── Jenkinsfile                     # Declarative pipeline executing CI/CD
├── README.md                       # High-fidelity architectural documentation
├── fintrack/                       # Core Flask application source
│   ├── app.py                      # Application entry point & factory
│   ├── config.py                   # Configuration environment loaders
│   ├── extensions.py               # Flask plugin instantiations (DB, Bcrypt, Login)
│   ├── requirements.txt            # Python dependencies manifest
│   ├── models/                     # SQLAlchemy database schemas (User, Budget, Income, Expense)
│   ├── routes/                     # Blueprint handlers (Auth, Dashboard, Expense, Income)
│   ├── static/                     # CSS stylesheets and interactive client scripts
│   ├── templates/                  # Jinja2 HTML layout views
│   └── tests/                      # Automated unit test files
│       └── test_app.py             # Test assertions for routes and config
├── k8s/                            # Kubernetes manifest configurations
│   ├── fintrack-deployment.yaml    # Application deployment & load-balancer service
│   ├── fintrack-service.yaml       # Isolated app service definition
│   ├── prometheus.yaml             # Prometheus deployment, namespace, config map, service
│   └── grafana.yaml                # Grafana server, namespace, service
└── result/                         # Build artifacts and status captures
    ├── flow_diagram.png            # Static system flow diagram
    └── jenkins_pipeline.png        # Screenshot of successful Jenkins pipeline run
```

---

## 🔌 API Route Catalog

The application exposes the following web interfaces and API routes:

| Module | Route / Endpoint | HTTP Method(s) | Auth Required | Description |
| :--- | :--- | :--- | :---: | :--- |
| **Authentication** | `/register` | `GET`, `POST` | ❌ No | Renders signup view and handles user registrations |
| **Authentication** | `/login` | `GET`, `POST` | ❌ No | Authenticates user credentials and starts session |
| **Authentication** | `/logout` | `GET` |  Yes | Terminates session and redirects to login |
| **Dashboard** | `/` | `GET` |  Yes | Root route; redirects to user finance dashboard |
| **Dashboard** | `/dashboard` | `GET` |  Yes | Main dashboard showing account balances and summaries |
| **Dashboard** | `/seed_data` | `GET` |  Yes | Seeds mock transactions for quick verification |
| **Dashboard** | `/reports` | `GET` |  Yes | Displays monthly spending trends and categoric charts |
| **Expenses** | `/expenses` | `GET`, `POST` |  Yes | Lists recent expenses; handles new expense submissions |
| **Expenses** | `/expense/delete/<id>` | `POST` |  Yes | Deletes a specific expense record (owner only) |
| **Income** | `/income` | `GET`, `POST` |  Yes | Lists recent income records; handles new income logs |
| **Income** | `/income/delete/<id>` | `POST` |  Yes | Deletes a specific income record (owner only) |

---

## 🛠️ Local Development & Environment Setup

To run the application locally outside of a Docker container:

### 1. Environment Activation
Clone the repository and set up a virtual sandbox to prevent dependency conflicts:
```bash
git clone https://github.com/VishnuSaravanan335/fintrack.git
cd fintrack

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate
```

### 2. Dependency Resolution
Install python requirements from [requirements.txt](file:///w:/fintrack/fintrack/requirements.txt):
```bash
pip install -r fintrack/requirements.txt
```

### 3. Execution
Start the development server with debug mode enabled:
```bash
cd fintrack
python app.py
```
Open **`http://localhost:5000`** in your web browser.

### 4. Running the Test Suite
Trigger the test discovery suite using `pytest`:
```bash
pytest tests/
```

---

## 🐳 Containerization with Docker

To build and test the production-ready Docker image locally:

### 1. Build Image
```bash
docker build -t fintrack-flask:latest .
```

### 2. Run Container
Map host port `5000` to the containerized Flask port `5000`:
```bash
docker run -d -p 5000:5000 --name fintrack-container fintrack-flask:latest
```
Access the application at: **`http://localhost:5000`**

---

## ⚙️ CI/CD Pipeline (Jenkins Declarative Engine)

The pipeline is defined in the declarative [Jenkinsfile](file:///w:/fintrack/Jenkinsfile) and processes code pushes automatically:

| Stage | Actions & Scripts | Output / Goal |
| :--- | :--- | :--- |
| **1. Clone Repository** | `git branch: 'main', url: '...'` | Synchronizes the workspace with the latest commits |
| **2. Run Tests** | `cd fintrack && pytest` | Executes unit tests and assertions on routes and configs |
| **3. Build Image** | `docker build -t fintrack:$BUILD_NUMBER .` | Packages code into a versioned, immutable Docker image |
| **4. ECR Push** | `docker push $REGISTRY/fintrack:$BUILD_NUMBER` | Pushes the image to Amazon ECR after AWS authentication |
| **5. Kubernetes Deploy** | `kubectl apply -f k8s/fintrack-deployment.yaml` | Performs a rolling update of pods with zero-downtime |
| **6. Monitoring Setup** | `kubectl apply -f k8s/grafana.yaml` | Applies Grafana deployment within the monitoring namespace |

---

## ☸️ Production Kubernetes Deployments

The orchestration layer uses two primary configuration files:
*   [k8s/fintrack-deployment.yaml](file:///w:/fintrack/k8s/fintrack-deployment.yaml): Configures a `Deployment` specifying `replicas: 2` for high availability and rolling update strategies.
*   [k8s/fintrack-service.yaml](file:///w:/fintrack/k8s/fintrack-service.yaml): Configures a `Service` of type `LoadBalancer` to route external traffic to container port `5000`.

To apply these manifest configurations manually:
```bash
kubectl apply -f k8s/fintrack-deployment.yaml
kubectl apply -f k8s/fintrack-service.yaml
```

---

## 📊 Observability (Prometheus & Grafana)

The monitoring infrastructure operates within a dedicated `monitoring` namespace.

1.  **Prometheus Setup:**
    Deploys a Prometheus server configured to scrape app metrics from the cluster's endpoints:
    ```bash
    kubectl apply -f k8s/prometheus.yaml
    ```
2.  **Grafana Visualization:**
    Deploys Grafana on the cluster:
    ```bash
    kubectl apply -f k8s/grafana.yaml
    ```
    *   **NodePort Access:** Access Grafana at `http://<Node-IP>:30300`.
    *   **Configuration:** Add Prometheus (`http://prometheus-service.monitoring.svc.cluster.local:80`) as a data source inside Grafana to visualize metrics.

---

## 🔒 Production Readiness & Best Practices

To adapt this setup for live production environments, consider the following recommendations:

1.  **Configure a Production WSGI Server:**
    Avoid running `python app.py` (which uses Flask's built-in single-threaded server) in production. Instead, utilize **Gunicorn**:
    ```bash
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
    ```
    Update the `CMD` instruction in your `Dockerfile` accordingly.

2.  **External Secrets Management:**
    Instead of exposing credentials in env config files, store credentials using **AWS Secrets Manager** or **Kubernetes Secrets** and inject them dynamically at runtime.

3.  **Database Migration Strategy:**
    Integrate **Flask-Migrate** (Alembic) to handle database schema migrations seamlessly without losing user table records.

---

## 🏆 Visual Captures

### CI/CD Architecture Flowchart
![CI/CD Pipeline Flow Diagram](result/flow_diagram.png)

### Jenkins Build Log Verification
![Jenkins Pipeline Success](result/jenkins_pipeline.png)
