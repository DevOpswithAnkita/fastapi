# FastAPI – Docker Setup Guide

This guide explains how to build, scan, and run a **FastAPI** application using **Docker** and **Docker Compose**.

---

##  Docker Image Build

Build the Docker image using a custom Dockerfile location:

```bash
docker build -t docker-fastapi:latest -f docker/dockerfile .
```

---

##  Docker Login

Login to Docker Hub (required for Docker Scout):

```bash
docker login
```

---

##  Image Security Scan (Docker Scout)

Check vulnerabilities and security recommendations:

```bash
# View CVEs
docker scout cves docker-fastapi:latest

# Quick vulnerability summary
docker scout quickview docker-fastapi:latest

# Hardening & optimization recommendations
docker scout recommendations docker-fastapi:latest
```

---

##  Run Container (Without Docker Compose)

Run the container and expose FastAPI on port **8000**:

```bash
docker run -p 8000:8000 docker-fastapi:latest
```

Access the app:

```
http://localhost:8000
```

---

##  Run Using Docker Compose

### Step 1: Navigate to docker directory

```bash
cd docker
```

### Step 2: Build & Run Containers

**Foreground mode:**

```bash
docker compose up --build
```

**Background (detached) mode:**

```bash
docker compose up -d --build
```

---

##  Rebuild Without Cache

```bash
docker compose build --no-cache
docker compose up -d
```

---

##  Stop Containers

```bash
docker compose down
```

---

##  Custom Domain Access (Optional)

Add the following entry to `/etc/hosts`:

```bash
127.0.0.1 example.com www.example.com
```

Then access the application via:

```
http://example.com
```

---

 **FastAPI Docker setup is complete!**
