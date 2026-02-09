# FastAPI Kubernetes Deployment

A complete guide to deploy FastAPI application on Kubernetes using Minikube with NGINX Ingress.

##  Prerequisites

- Docker installed (https://www.docker.com/get-started/)
- Minikube installed (https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable)
- kubectl installed (https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- Basic knowledge of Kubernetes

## Quick Start

### 1. Start Minikube

```bash
minikube start
```

### 2. Configure Docker Environment (Optional - for local builds)

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)
```

### 3. Build Docker Image

**Option A: Build locally for Minikube**
```bash
docker build -f docker/dockerfile -t docker-fastapi:latest .
```

**Option B: Build and push to Docker Hub**
```bash
# Build image
docker build -f docker/dockerfile -t your-username/docker-fastapi:latest .

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push your-username/docker-fastapi:latest

# Verify image
docker image ls
```

**Optional: Scan image for vulnerabilities**
```bash
docker scout quickview docker-fastapi:latest
```

##  Kubernetes Deployment

### Deploy All Resources

```bash
# Navigate to k8s directory
cd k8s

# Apply all configurations at once
kubectl apply -f .
```

### Or Deploy Step-by-Step

```bash
# 1. Create namespace
kubectl apply -f namespace.yaml

# 2. Apply ConfigMap
kubectl apply -f configmap.yaml

# 3. Deploy application
kubectl apply -f deployment.yaml

# 4. Create service
kubectl apply -f service.yaml

# 5. Configure Ingress
kubectl apply -f ingress.yaml
```

### Verify Deployment

```bash
# Check all resources in namespace
kubectl get all -n fastapi-ns

# Check pods status
kubectl get pods -n fastapi-ns

# Check service
kubectl get svc -n fastapi-ns

# Check ingress
kubectl get ingress -n fastapi-ns
```

## Accessing the Application

### Method 1: Minikube Service (Recommended for quick testing)

```bash
minikube service fastapi-svc -n fastapi-ns
```
This command automatically opens your application in the browser.

### Method 2: Port Forwarding (Simple local access)

**Access via Service:**
```bash
kubectl port-forward svc/fastapi-svc 8000:80 -n fastapi-ns
```
Then visit: http://localhost:8000

**Access via Ingress Controller:**
```bash
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8000:80
```
Then use one of these methods:

**With curl (using Host header):**
```bash
curl -H "Host: example.com" http://localhost:8000
```

**In browser:**
- Visit: http://localhost:8000
- Or add to `/etc/hosts`: `127.0.0.1 example.com`
- Then visit: http://example.com

### Method 3: NodePort (Direct cluster access)

```bash
# Get Minikube IP
minikube ip

# Get NodePort
kubectl get svc fastapi-svc -n fastapi-ns
# Look for port mapping like: 80:30297/TCP

# Access in browser
# http://<minikube-ip>:<nodeport>
# Example: http://192.168.49.2:30297
```

### Method 4: Ingress with Minikube Tunnel (Production-like setup)

**Step 1: Enable NGINX Ingress Controller**
```bash
minikube addons enable ingress
```

**Step 2: Update /etc/hosts**
```bash
# Get Minikube IP
minikube ip
# Example output: 192.168.49.2

# Edit hosts file
sudo nano /etc/hosts

# Add these lines (replace with your Minikube IP):
192.168.49.2  example.com
192.168.49.2  www.example.com
```

**Step 3: Start Minikube Tunnel**
```bash
# Run in separate terminal (keep it running)
minikube tunnel
# Enter password when prompted
```

**Step 4: Access Application**
```bash
# Test with curl
curl http://example.com

# Or open in browser
open http://example.com
```

**If tunnel already running:**
```bash
# Check tunnel status
ps aux | grep "minikube tunnel"

# Kill existing tunnel if needed
sudo pkill -f "minikube tunnel"

# Start new tunnel
minikube tunnel
```

## Debugging & Troubleshooting

### Check Pod Logs
```bash
# View logs for all pods
kubectl logs -n fastapi-ns -l app=fastapi-deployment

# View logs for specific pod
kubectl logs -n fastapi-ns <pod-name>

# Follow logs in real-time
kubectl logs -n fastapi-ns -l app=fastapi-deployment -f
```

### Check Ingress Status
```bash
# Describe ingress for details
kubectl describe ingress fastapi-ingress -n fastapi-ns

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller --tail=50
```

### Check Service Endpoints
```bash
# Verify service has endpoints
kubectl get endpoints fastapi-svc -n fastapi-ns

# Should show pod IPs like: 10.244.0.96:8000,10.244.0.98:8000
```

### Common Issues

**Issue: Ingress not working**
```bash
# Verify NGINX Ingress Controller is installed
kubectl get pods -n ingress-nginx

# If not installed, enable it
minikube addons enable ingress

# Check if IngressClass exists
kubectl get ingressclass
```

**Issue: "Connection refused" or "404 Not Found"**
```bash
# Check if pods are running
kubectl get pods -n fastapi-ns

# Verify service is routing correctly
kubectl describe svc fastapi-svc -n fastapi-ns

# Test service directly
kubectl port-forward svc/fastapi-svc 8000:80 -n fastapi-ns
curl http://localhost:8000
```

**Issue: DNS not resolving (example.com)**
```bash
# Verify /etc/hosts entry
cat /etc/hosts | grep example.com

# Clear DNS cache (macOS)
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# Test DNS resolution
ping example.com
# Should show: PING example.com (192.168.49.2)
```

## Cleanup

```bash
# Delete all resources in namespace
kubectl delete -f k8s/

# Or delete namespace (removes everything)
kubectl delete namespace fastapi-ns

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

##  Project Structure

```
.
├── docker/
│   └── dockerfile          # Docker build configuration
├.      docker-compose.yml
├── k8s/
│   ├── namespace.yaml      # Kubernetes namespace
│   ├── configmap.yaml      # Configuration data
│   ├── deployment.yaml     # Application deployment
│   ├── service.yaml        # Service configuration
│   └── ingress.yaml        # Ingress rules
|        README.md
├── nginx/
│   └── nginx.conf          # NGINX configuration (for Docker Compose)
├── app/
│   └── ...                 # FastAPI application code
└── README.md
```

##  Configuration Details

### Service Configuration
- **Type:** NodePort
- **Port:** 80 (external)
- **TargetPort:** 8000 (container)
- **Selector:** app=fastapi-deployment

### Ingress Configuration
- **Class:** nginx
- **Hosts:** example.com, www.example.com, localhost
- **Backend:** fastapi-svc:80
- **Annotation:** rewrite-target: /

##  Useful Commands

```bash
# Get all resources across all namespaces
kubectl get all --all-namespaces

# Watch pod status in real-time
kubectl get pods -n fastapi-ns -w

# Execute command in pod
kubectl exec -it -n fastapi-ns <pod-name> -- /bin/bash

# Get detailed pod information
kubectl describe pod -n fastapi-ns <pod-name>

# Scale deployment
kubectl scale deployment fastapi-deployment -n fastapi-ns --replicas=3

# Restart deployment
kubectl rollout restart deployment fastapi-deployment -n fastapi-ns

# Check deployment rollout status
kubectl rollout status deployment fastapi-deployment -n fastapi-ns
```
