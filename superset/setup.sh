
docker exec -it bi_superset superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@localhost \
              --password secret

docker exec -it bi_superset superset db upgrade &&
         docker exec -it bi_superset superset init