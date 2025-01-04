
docker build -t simple-flask .

docker run -dt -p 8080:8080 simple-flask

docker ps

docker stop <CONTAINER ID>