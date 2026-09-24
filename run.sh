xhost +local:docker
docker compose up -d microros
docker exec -it uros2_env /bin/bash
docker compose down
