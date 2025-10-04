from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Create Spark session
spark = SparkSession.builder \
    .appName("SparkKafkaStreamingTest") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read streaming data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "test-topic") \
    .load()

# Convert binary Kafka "value" column to string
messages = df.selectExpr("CAST(value AS STRING) as message")

# Write stream to console
query = messages.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
