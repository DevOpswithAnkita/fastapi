# fastapi
#docker build 
docker build -t docker-fastapi:latest -f docker/dockerfile .
# View a summary of image vulnerabilities and recommendations → docker scout quickview
docker login
docker scout cves docker-fastapi:latest
docker scout quickview docker-fastapi:latest
docker scout recommendations docker-fastapi:latest
# Run Container
docker run -p 8000:8000 docker-fastapi:latest

#run using  docker-compose.yml
# Go to docker/ directory 
cd docker
# Build  run  (foreground )
docker compose up --build
# Build  run (background )
docker compose up -d --build
# Rebuild without cache
docker compose build --no-cache
docker compose up -d
# Container stop 
docker compose down

<!-- cat /etc/hosts
127.0.0.1 example.com www.example.com -->