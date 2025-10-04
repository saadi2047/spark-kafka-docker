#!/bin/bash
set -e

echo "───────────────────────────────────────────────"
echo " 🔁 Spark–Kafka–MySQL Environment Recovery"
echo "───────────────────────────────────────────────"

cd ~/spark-kafka-docker

# 1️⃣ Stop and clean any old containers
echo "[1/6] Cleaning up old containers..."
docker-compose down -v || true

# 2️⃣ Start all services
echo "[2/6] Starting Docker Compose stack..."
docker-compose up -d

# 3️⃣ Wait for containers to stabilize
echo "[3/6] Waiting for containers to come up..."
sleep 15

# 4️⃣ Verify running services
echo "[4/6] Checking running containers..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 5️⃣ Recreate Kafka test-topic (if missing)
echo "[5/6] Ensuring Kafka test-topic exists..."
docker exec -i kafka-tools kafka-topics --bootstrap-server kafka:9092 --list | grep -q test-topic \
  || docker exec -i kafka-tools kafka-topics --bootstrap-server kafka:9092 --create --topic test-topic --partitions 1 --replication-factor 1

# 6️⃣ Produce a few test messages
echo "[6/6] Sending quick test messages to Kafka..."
docker exec -i kafka-tools bash -c "echo -e 'restart-check-1\nrestart-check-2\nrestart-check-3' | kafka-console-producer --broker-list kafka:9092 --topic test-topic"

echo ""
echo "✅ Environment recovered successfully!"
echo "───────────────────────────────────────────────"
echo "Spark Master UI:       http://localhost:8080"
echo "Spark Worker UI:       http://localhost:8081"
echo "Spark History Server:  http://localhost:18080"
echo "MySQL (host):          localhost:3307 (user: sparkuser, pass: sparkpass)"
echo "Kafka topic validated: test-topic"
echo "──────────Saadi M M─────────────────────────────────────"
