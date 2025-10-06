from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("Table_Comparison_ETL")
    .master("spark://spark-master:7077")
    .config("spark.jars.packages",
            "mysql:mysql-connector-java:8.0.33")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Connection details
url = "jdbc:mysql://mysql:3306/testdb"
props = {"user": "sparkuser", "password": "sparkpass", "driver": "com.mysql.cj.jdbc.Driver"}

# Read both tables
df1 = spark.read.jdbc(url=url, table="table1", properties=props)
df2 = spark.read.jdbc(url=url, table="table2", properties=props)

# Find mismatched rows (full outer join on key)
join_cond = df1.id == df2.id
comparison = (
    df1.alias("a")
    .join(df2.alias("b"), join_cond, "full_outer")
    .select(
        col("a.id").alias("id_a"),
        col("a.name").alias("name_a"),
        col("a.amount").alias("amount_a"),
        col("b.id").alias("id_b"),
        col("b.name").alias("name_b"),
        col("b.amount").alias("amount_b")
    )
    .where(
        (col("id_a").isNull()) | (col("id_b").isNull()) |
        (col("amount_a") != col("amount_b")) |
        (col("name_a") != col("name_b"))
    )
)

# Write results back to MySQL
(
    comparison.write
    .format("jdbc")
    .option("url", url)
    .option("dbtable", "table_compare_result")
    .option("user", "sparkuser")
    .option("password", "sparkpass")
    .option("driver", "com.mysql.cj.jdbc.Driver")
    .mode("overwrite")
    .save()
)

spark.stop()
