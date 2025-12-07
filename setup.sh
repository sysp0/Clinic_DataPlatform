#!/bin/bash

cp .env.example .env
docker compose up -d
echo "Waiting for services to start..."
sleep 20
./superset/setup.sh

echo ""
echo "=================================="
echo "         SERVICES READY"
echo "=================================="
echo ""
echo "AirFlow:"
echo "  URL: http://localhost:8080"
echo "  User: admin"
echo "  Pass: `docker exec -it bi_airflow cat simple_auth_manager_passwords.json.generated` "
echo ""
echo "Superset:"
echo "  URL: http://localhost:8088"
echo "  User: admin"
echo "  Pass: secret"
echo ""
echo "=================================="