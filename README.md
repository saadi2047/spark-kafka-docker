# 🔥 Spark–Kafka–MySQL Observability Stack (E-PAY 2.0)
# 🚀 Spark-Kafka-MySQL ETL Pipeline with Airflow & Loki/Grafana (E-PAY 2.0 POC)

This repository contains a **complete end-to-end data engineering stack** built using Docker Compose — integrating **Apache Spark**, **Kafka (KRaft mode)**, **MySQL**, **Apache Airflow**, and **Grafana Loki/Promtail** for centralized logging and monitoring.

Designed and implemented as part of the **E-PAY 2.0 project** — for SBI in collaboration with Red Hat — this POC demonstrates real-time data ingestion, ETL processing, job orchestration, and log visualization in a containerized environment.

---

## 🏗️ **Architecture Overview**
           ┌───────────────────────────────┐
           │         Apache Airflow         │
           │   (Job Orchestrator & DAG UI)  │
           └──────────────┬────────────────┘
                          │ triggers
                          ▼
    ┌──────────────────────────────────────────────┐
    │                 Apache Spark                 │
    │  spark-master + spark-worker + history-server│
    │  runs ETL jobs via JDBC over MySQL           │
    └──────────────┬───────────────────────────────┘
                   │
                   ▼
             ┌──────────────┐
             │    MySQL     │
             │ Source + Sink│
             │ (table1, table2, result) │
             └──────────────┘
                   │
                   ▼
           ┌────────────────────┐
           │   Apache Kafka     │
           │ (KRaft mode broker)│
           └────────────────────┘
                   │
                   ▼
           ┌──────────────────────┐
           │ Loki + Promtail + Grafana │
           │   Centralized Log View UI │
           └──────────────────────┘





---

## 🧰 **Tech Stack**

| Component | Description |
|------------|-------------|
| **Apache Spark 4.0.0** | ETL engine for comparing and transforming large datasets |
| **Apache Kafka 3.7.0 (KRaft)** | Message broker (no Zookeeper) |
| **MySQL 8.0.43** | Source and sink database for ETL |
| **Apache Airflow 2.10.2** | Workflow orchestration for Spark jobs |
| **Grafana + Loki + Promtail** | Monitoring and log aggregation |
| **Docker Compose** | Container orchestration for all services |

---

## ⚙️ **1. Prerequisites**

- Docker ≥ 24.x  
- Docker Compose ≥ 2.x  
- Minimum 8 GB RAM (recommended 12 GB for full stack)
- Linux/WSL2 environment

---

## 🧩 **2. Repository Structure**
spark-kafka-docker/
├── airflow/
│ ├── dags/
│ │ ├── compare_tables_dag.py # Airflow DAG to run Spark ETL
│ │ └── spark_kafka_mysql_dag.py # Kafka → Spark → MySQL DAG
│ ├── logs/
│ └── plugins/
│
├── dags/ # Optional DAG mounts
├── loki/config.yaml # Loki configuration
├── promtail/config.yml # Promtail log collection config
│
├── table_compare_etl.py # PySpark ETL script (table1 vs table2)
│
├── docker-compose.yml # Spark + Kafka + MySQL stack
├── docker-compose.airflow.yml # Airflow orchestration layer
├── docker-compose.loki.yml # Loki, Promtail & Grafana monitoring
│
├── jars/ # MySQL JDBC connector (if needed)
├── logs/ # Local log mounts
└── README.md



---

## 🐳 **3. Bring up the environment**

### Step 1 – Start core stack (Spark + Kafka + MySQL)
```bash
docker-compose up -d


Step 2 – Start Airflow stack

docker-compose -f docker-compose.airflow.yml up -d


Step 3 – Start Loki + Promtail + Grafana
Step 3 – Start Loki + Promtail + Grafana
docker-compose -f docker-compose.loki.yml up -d

check containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"


4. MySQL Database Setup

Connect to MySQL:

docker exec -it mysql mysql -usparkuser -psparkpass testdb

Create tables for ETL:
Create tables for ETL:
CREATE TABLE table1 (id INT, name VARCHAR(50), amount INT);
CREATE TABLE table2 (id INT, name VARCHAR(50), amount INT);
CREATE TABLE table_compare_result AS SELECT * FROM table1 WHERE 1=0;

INSERT INTO table1 VALUES (1,'Alice',100), (2,'Bob',200), (3,'Charlie',300);
INSERT INTO table2 VALUES (1,'Alice',100), (2,'Bob',250), (3,'Charlie',300);


⚡ 5. ETL Job: Compare Two Tables

table_compare_etl.py uses Spark to:

Compare two large tables (table1, table2)

Identify mismatched or missing rows

Store results into table_compare_result

docker exec -it spark-master \
  spark-submit \
  --master spark://spark-master:7077 \
  --jars /opt/spark/jars/mysql-connector-java-8.0.33.jar \
  /opt/spark/work-dir/table_compare_etl.py


🪶 6. Orchestrate via Airflow

Access Airflow Web UI:

http://localhost:8080

Username: admin
Password: admin

Enable and trigger DAG:

compare_tables_dag

check via cli
docker exec airflow-webserver airflow dags list
docker exec airflow-scheduler airflow dags trigger compare_tables_dag
docker exec airflow-scheduler airflow dags list-runs -d compare_tables_dag



📊 7. Logs & Monitoring

Access Grafana:

http://localhost:3000

Username: admin
Password: admin

✅ Loki endpoint automatically configured at http://loki:3100
✅ Promtail collects container logs from /var/lib/docker/containers

You can filter logs by container:


{container_name="spark-master"}
{container_name="airflow-webserver"}


🧠 8. Validation

Check ETL output in MySQL:

docker exec -it mysql mysql -usparkuser -psparkpass testdb
SELECT * FROM table_compare_result;


Expected result:

id_a	name_a	amount_a	id_b	name_b	amount_b
2	Bob	200	2	Bob	250
🛠 9. Common Commands
Action	Command
Rebuild all containers	docker-compose down -v && docker-compose up -d
View logs for a service	docker logs spark-master -f
Restart Airflow only	docker-compose -f docker-compose.airflow.yml restart
Stop everything	docker-compose down && docker-compose -f docker-compose.airflow.yml down && docker-compose -f docker-compose.loki.yml down
📦 10. Future Enhancements

Add Kafka → Spark streaming DAGs (CDC / real-time data diff)

Push ETL metadata to DynamoDB or S3

Enable Spark History Server S3 integration

Add Grafana dashboard JSON templates

Integrate Red Hat Service Mesh for distributed tracing

🧑‍💻 Author



Saadi Muzzammil
DevOps / Data Engineering – E-PAY 2.0 Project (SBI x Red Hat)
📧 github.com/saadi2047

🏁 License

MIT License © 2025 Saadi Muzzammil































Complete end-to-end environment for streaming ETL + monitoring:
- **Apache Spark** (master + worker + history)
- **Kafka 3.7.0 (KRaft mode)**
- **MySQL 8.0**
- **Airflow** for orchestration
- **Grafana + Loki + Promtail** for centralized logs

---

## 🧩 Quick Start

```bash
# Core stack
docker-compose up -d
# Airflow
docker-compose -f docker-compose.airflow.yml up -d
# Observability
docker-compose -f docker-compose.loki.yml up -d


🌐 Access URLs
Service	URL	Notes
Spark Master	http://localhost:8081
	Spark UI
Spark Worker	http://localhost:8082
	Worker UI
History Server	http://localhost:18080
	Job logs
Airflow UI	http://localhost:8080
	Scheduler/DAGs
Grafana	http://localhost:3000
	admin/admin
Loki	http://localhost:3100
	log API



🧠 Future Enhancements

Add Prometheus + Node Exporter for metrics

Deploy to OpenShift or EKS for DR testing

Integrate CI/CD via GitHub Actions



Save it, commit, and push:
```bash
git add README.md
git commit -m "📝 Updated README with observability and access info"
git push







# spark-kafka-docker
Complete Spark 4 + Kafka 3.7 + MySQL 8 + History Server setup



spark-kafka-docker/
├── docker-compose.yml                # Spark + Kafka + MySQL core
├── docker-compose.airflow.yml        # Airflow orchestration
├── docker-compose.loki.yml           # Grafana + Loki + Promtail stack
├── loki/
│   └── config.yaml                   # Loki v3.0.0 config (fixed)
├── promtail/
│   └── config.yml                    # Promtail log collector config
├── airflow/
│   ├── dags/
│   ├── logs/
│   └── plugins/
├── dags/                             # optional DAGs dir (duplicate safe)
├── jars/                             # Spark JARs if needed
├── logs/                             # local container logs
├── streaming-etl.py                  # your ETL script (Kafka→Spark→MySQL)
├── streaming-test.py                 # your test consumer script
├── restart-recovery.sh               # helper script for restart
├── .gitignore                        # will add below
└── README.md                         # repo documentation
