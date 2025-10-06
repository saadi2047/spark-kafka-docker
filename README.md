# 🔥 Spark–Kafka–MySQL Observability Stack (E-PAY 2.0)

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
