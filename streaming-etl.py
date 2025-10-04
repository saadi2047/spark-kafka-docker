from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, current_timestamp

# ---- Spark session ----
spark = (
    SparkSession.builder
    .appName("KafkaToMySQL_ETL")
    .master("spark://spark-master:7077")
    # Optional: Kryo usually avoids Java-serializer hiccups
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# ---- Read from Kafka ----
raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "test-topic")
    .option("startingOffsets", "latest")
    .load()
)

# value is binary → string
msgs = raw.selectExpr("CAST(value AS STRING) AS message")

# Parse "key=value" messages
parsed = (
    msgs
    .withColumn("key_col", split(col("message"), "=", -1)[0])
    .withColumn("value_col", split(col("message"), "=", -1)[1])
    .withColumn("processed_at", current_timestamp())
    .select("key_col", "value_col", "processed_at")
)

jdbc_url = "jdbc:mysql://mysql:3306/testdb"
jdbc_props = {
    "user": "sparkuser",
    "password": "sparkpass",
    "driver": "com.mysql.cj.jdbc.Driver",
}

def write_to_mysql(batch_df, batch_id):
    # No batch_df.count() — avoid triggering the serialization bug
    (
        batch_df
        .write
        .format("jdbc")
        .mode("append")
        .option("url", jdbc_url)
        .option("dbtable", "spark_stream_output")
        .option("user", jdbc_props["user"])
        .option("password", jdbc_props["password"])
        .option("driver", jdbc_props["driver"])
        .save()
    )

query = (
    parsed.writeStream
    .outputMode("append")
    .foreachBatch(write_to_mysql)
    .option("checkpointLocation", "/tmp/checkpoints/kafka_to_mysql")
    .start()
)

print("🚀 Kafka to MySQL streaming ETL started... Waiting for data.")
query.awaitTermination()

