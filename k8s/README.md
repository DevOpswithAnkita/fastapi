# Local testing  (Minikube)

minikube starteval $(minikube docker-env)
docker build -f docker/dockerfile -t docker-fastapi:latest .
docker login
docker scout quickview docker-fastapi:latest

# Docker Hub

docker build -f docker/dockerfile -t your-username/docker-fastapi:latest .
docker push your-username/docker-fastapi:latest
docker image ls

# Manual deployment

cd k8skubectl apply -f .

# Namespace create karein

kubectl apply -f namespace.yaml

# ConfigMap

kubectl apply -f configmap.yaml

# Deployment

kubectl apply -f deployment.yaml

# Service

kubectl apply -f service.yaml

# ALLresources check

kubectl get all -n fastapi-ns

# To check api is working or not

# Option 1: Minikube service command (recommended for local)
minikube service fastapi-svc -n fastapi-ns
# Tunnel (open)
sudo minikube tunnel

# Option 2: Port forwarding
kubectl port-forward svc/fastapi-svc 8000:80 -n fastapi-ns
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8000:80
curl -H "Host: example.com" http://localhost:8000# 
then browser : http://localhost:8000,http://example.com/

# Option 3: NodePort (Service NodePort type)
minikube ip  # IP 
kubectl get svc fastapi-svc -n fastapi-ns  # Port

# Browser mein: http://`<minikube-ip>`:`<nodeport>`
