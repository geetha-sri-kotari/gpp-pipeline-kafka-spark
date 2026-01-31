from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.appName("UserActivityPipeline").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("event_time", StringType()),
    StructField("user_id", StringType()),
    StructField("page_url", StringType()),
    StructField("event_type", StringType())
])

raw = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "user_activity") \
    .load()

events = raw.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select(
        to_timestamp("data.event_time").alias("event_time"),
        "data.user_id",
        "data.page_url",
        "data.event_type"
    ) \
    .withWatermark("event_time", "2 minutes")

# PAGE VIEWS (1 min tumbling)
page_views = events.filter(col("event_type") == "page_view") \
    .groupBy(
        window("event_time", "1 minute"),
        col("page_url")
    ).count()

page_views_query = page_views.writeStream \
    .foreachBatch(lambda df, _: df.write
        .format("jdbc")
        .option("url", "jdbc:postgresql://db:5432/stream_data")
        .option("dbtable", "page_view_counts")
        .option("user", "user")
        .option("password", "password")
        .mode("append")
        .save()
    ).start()

# ACTIVE USERS (5 min sliding)
active_users = events.groupBy(
    window("event_time", "5 minutes", "1 minute")
).agg(approx_count_distinct("user_id").alias("active_user_count"))

active_users_query = active_users.writeStream \
    .foreachBatch(lambda df, _: df.write
        .format("jdbc")
        .option("url", "jdbc:postgresql://db:5432/stream_data")
        .option("dbtable", "active_users")
        .option("user", "user")
        .option("password", "password")
        .mode("append")
        .save()
    ).start()

# DATA LAKE
events.withColumn("event_date", to_date("event_time")) \
    .writeStream \
    .format("parquet") \
    .option("path", "/opt/spark/data/lake") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .partitionBy("event_date") \
    .start()

# ENRICHED KAFKA
enriched = events.withColumn("processing_time", current_timestamp()) \
    .selectExpr("to_json(struct(*)) AS value")

enriched.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "enriched_activity") \
    .option("checkpointLocation", "/tmp/kafka-checkpoint") \
    .start()

spark.streams.awaitAnyTermination()
