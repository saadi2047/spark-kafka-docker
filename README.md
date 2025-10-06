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
