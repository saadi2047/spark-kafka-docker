from pyspark.sql import SparkSession
from pyspark.sql.functions import split, current_timestamp, col

# 1️⃣ Create Spark session
spark = SparkSession.builder \
    .appName("SparkKafkaMySQLPipeline") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2️⃣ Read streaming data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "test-topic") \
    .load()

# 3️⃣ Convert binary value to string
messages = df.selectExpr("CAST(value AS STRING) as message")

# 4️⃣ Split into key and value columns
parsed = messages.withColumn("key_col", split(col("message"), "=").getItem(0)) \
                 .withColumn("value_col", split(col("message"), "=").getItem(1)) \
                 .withColumn("processed_at", current_timestamp()) \
                 .select("key_col", "value_col", "processed_at")

# 5️⃣ Define write-to-MySQL logic
def write_to_mysql(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://mysql:3306/testdb") \
        .option("dbtable", "spark_stream_output") \
        .option("user", "sparkuser") \
        .option("password", "sparkpass") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .mode("append") \
        .save()

# 6️⃣ Write stream to both console & MySQL
query = parsed.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_mysql) \
    .option("truncate", "false") \
    .format("console") \
    .start()

query.awaitTermination()
