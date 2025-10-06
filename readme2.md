README.md — Spark-Kafka-MySQL ETL with Airflow + Loki/Grafana
# 🚀 Spark-Kafka-MySQL ETL Pipeline  
### with Apache Airflow + Loki/Promtail + Grafana  
*(E-PAY 2.0 POC for SBI × Red Hat)*

![Spark](https://img.shields.io/badge/Apache%20Spark-4.0.0-FF7F50?logo=apache-spark&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-3.7.0-black?logo=apache-kafka&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0.43-4479A1?logo=mysql&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.10.2-017CEE?logo=apache-airflow&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-11.1.0-F46800?logo=grafana&logoColor=white)
![Loki](https://img.shields.io/badge/Loki-3.0.0-00BFFF?logo=grafana&logoColor=white)
![Promtail](https://img.shields.io/badge/Promtail-3.0.0-00BFFF?logo=grafana&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

### 🧠 **About**

This repository provides a **complete end-to-end containerized data engineering environment** featuring:

- **Apache Spark** for batch ETL and comparison jobs  
- **Kafka (KRaft mode)** for real-time data streaming  
- **MySQL** as both the source and sink  
- **Apache Airflow** for job orchestration  
- **Grafana Loki + Promtail** for centralized log aggregation and visualization  

Built and optimized as part of the **E-PAY 2.0 modern banking pipeline** (State Bank of India × Red Hat).

---

## 🏗️ **Architecture**


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
             │ Source+Sink  │
             │ table1/table2│
             └──────────────┘
                   │
                   ▼
           ┌────────────────────┐
           │   Apache Kafka     │
           │   (KRaft broker)   │
           └────────────────────┘
                   │
                   ▼
           ┌──────────────────────────────┐
           │ Loki + Promtail + Grafana UI │
           │ Centralized log monitoring   │
           └──────────────────────────────┘


---

## 🧰 **Tech Stack**

| Component | Role |
|------------|------|
| **Apache Spark 4.0.0** | ETL & table comparison engine |
| **Apache Kafka 3.7.0 (KRaft)** | Messaging backbone (no Zookeeper) |
| **MySQL 8.0.43** | Source & sink DB |
| **Apache Airflow 2.10.2** | DAG orchestration & scheduler |
| **Grafana + Loki + Promtail** | Observability & log analytics |
| **Docker Compose** | Local orchestration of multi-service stack |

---

## ⚙️ **1️⃣ Prerequisites**

- Docker ≥ 24.x  
- Docker Compose ≥ 2.x  
- ≥ 8 GB RAM (recommended 12 GB)  
- Linux or WSL 2 environment

---

## 📁 **2️⃣ Repository Structure**



spark-kafka-docker/
├── airflow/
│ ├── dags/
│ │ ├── compare_tables_dag.py
│ │ └── spark_kafka_mysql_dag.py
│ ├── logs/
│ └── plugins/
│
├── loki/config.yaml
├── promtail/config.yml
├── table_compare_etl.py
│
├── docker-compose.yml
├── docker-compose.airflow.yml
├── docker-compose.loki.yml
├── jars/
├── logs/
└── README.md


---

## 🐳 **3️⃣ Deployment Steps**

### 🧩 Step 1 – Start Core Stack
```bash
docker-compose up -d

☁️ Step 2 – Start Airflow
docker-compose -f docker-compose.airflow.yml up -d

📊 Step 3 – Start Loki + Promtail + Grafana
docker-compose -f docker-compose.loki.yml up -d


Check:

docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

💾 4️⃣ Database Initialization
docker exec -it mysql mysql -usparkuser -psparkpass testdb

CREATE TABLE table1 (id INT, name VARCHAR(50), amount INT);
CREATE TABLE table2 (id INT, name VARCHAR(50), amount INT);
CREATE TABLE table_compare_result AS SELECT * FROM table1 WHERE 1=0;

INSERT INTO table1 VALUES (1,'Alice',100),(2,'Bob',200),(3,'Charlie',300);
INSERT INTO table2 VALUES (1,'Alice',100),(2,'Bob',250),(3,'Charlie',300);

⚡ 5️⃣ ETL Script: Table Comparison

table_compare_etl.py runs Spark ETL to:

Read table1 and table2

Compare records and detect mismatches

Write output to table_compare_result

Manual run:

docker exec -it spark-master \
  spark-submit \
  --master spark://spark-master:7077 \
  --jars /opt/spark/jars/mysql-connector-java-8.0.33.jar \
  /opt/spark/work-dir/table_compare_etl.py

🪶 6️⃣ Airflow Orchestration

Web UI → http://localhost:8080

Username: admin  Password: admin

Enable & trigger compare_tables_dag
or via CLI:

docker exec airflow-scheduler airflow dags trigger compare_tables_dag
docker exec airflow-scheduler airflow dags list-runs -d compare_tables_dag

📈 7️⃣ Logs & Monitoring

Grafana → http://localhost:3000

Username: admin Password: admin

Loki endpoint: http://loki:3100

Query examples:

{container_name="spark-master"}
{container_name="airflow-webserver"}

🧠 8️⃣ Validate Output
docker exec -it mysql mysql -usparkuser -psparkpass testdb
SELECT * FROM table_compare_result;


Expected result:

id_a	name_a	amount_a	id_b	name_b	amount_b
2	Bob	200	2	Bob	250
🛠 9️⃣ Handy Commands
Action	Command
Rebuild all	docker-compose down -v && docker-compose up -d
View logs	docker logs spark-master -f
Restart Airflow	docker-compose -f docker-compose.airflow.yml restart
Stop all	docker-compose down && docker-compose -f docker-compose.airflow.yml down && docker-compose -f docker-compose.loki.yml down
🚀 🔟 Next Enhancements

Add Kafka → Spark streaming DAG (CDC)

Push ETL metadata to S3/DynamoDB

Integrate Service Mesh (Kiali/Istio)

Create Grafana dashboard JSONs

Add email alerts from Airflow for ETL status

👨‍💻 Author

Saadi Muzzammil
DevOps & Data Engineering — E-PAY 2.0 (SBI × Red Hat)
📦 GitHub: saadi2047

🪪 License

MIT License © 2025 Saadi Muzzammil


---

### ✅ Next Recommendation
Once you add this file:
```bash
mv README.md README_with_badges.md
mv README_with_badges.md README.md
git add README.md
git commit -m "Added badge-style README with full documentation"
git push origin main
