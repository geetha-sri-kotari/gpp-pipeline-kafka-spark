FROM apache/spark:3.5.0

USER root

# Install Python (required for PySpark)
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

ENV PYSPARK_PYTHON=python
ENV PYSPARK_DRIVER_PYTHON=python

WORKDIR /app

CMD /opt/spark/bin/spark-submit \
 --master local[*] \
 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.1 \
 /app/spark_streaming_app.py
