# ---------------------------------------------------------
#  Base Spark 4.0.0 image with Java 21 + Python 3
#  Adds: Kafka client JARs, Hadoop-AWS, AWS SDK, MySQL JDBC
# ---------------------------------------------------------

FROM apache/spark:4.0.0-java21-python3

# Switch to root for installing packages
USER root
WORKDIR /opt/spark/work-dir

# Install useful OS tools
RUN apt-get update && apt-get install -y curl wget unzip vim && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------
#  Download common connectors and place into Spark jars
# ---------------------------------------------------------
RUN mkdir -p /opt/spark/jars && cd /opt/spark/jars && \
    wget -q https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.7.0/kafka-clients-3.7.0.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar && \
    wget -q https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.748/aws-java-sdk-bundle-1.12.748.jar && \
    wget -q https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar

# ---------------------------------------------------------
#  Environment variables
# ---------------------------------------------------------
ENV SPARK_HOME=/opt/spark
ENV PATH="$SPARK_HOME/bin:$PATH"

# Ensure the Spark entrypoint is executable
RUN chmod +x /opt/entrypoint.sh

# Default command
CMD ["/opt/entrypoint.sh"]
