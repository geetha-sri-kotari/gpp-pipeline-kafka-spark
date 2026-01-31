# Real-Time Data Pipeline using Kafka, Spark and PostgreSQL

## Project Overview

This project implements a real-time data pipeline in which user activity events are:

1. Produced to Apache Kafka
2. Consumed and processed using Apache Spark Structured Streaming
3. Stored in PostgreSQL for persistent storage

All services are containerized using Docker and orchestrated with Docker Compose.

---

## System Architecture

Producer (Python)
→ Kafka Topic
→ Spark Structured Streaming
→ PostgreSQL Database

---

## Technologies Used

* Apache Kafka – Event streaming
* Apache Zookeeper – Kafka coordination
* Apache Spark 3.5 – Stream processing
* PostgreSQL – Relational database
* Docker and Docker Compose – Containerization
* Python (PySpark) – Streaming logic

---

## Project Structure

```
gpp-pipeline-kafka-spark/
│
├── docker-compose.yml
├── .env
├── README.md
│
├── producer.py
├── init-db.sql
│
└── spark/
    ├── Dockerfile
    └── spark_streaming_app.py
```

---

## Environment Configuration

Create a `.env` file in the root directory:

```env
DB_USER=user
DB_PASSWORD=password
DB_NAME=stream_data
```

---

## How to Execute the Project

### Prerequisites

* Docker installed
* Docker Compose installed

Verify installation:

```bash
docker --version
docker compose version
```

---

### Start the Services

From the project root directory:

```bash
docker compose --env-file .env up --build
```

This command starts:

* Zookeeper
* Kafka
* PostgreSQL
* Spark Streaming Application

---

### Verify Containers

```bash
docker ps
```

Expected running containers:

* zookeeper
* kafka
* db
* spark-app

---

### Run Kafka Producer

Open a new terminal and execute:

```bash
docker exec -it kafka bash
```

Inside the Kafka container:

```bash
python3 /producer.py
```

This sends sample messages to the Kafka topic.

---

## Database Verification

Connect to PostgreSQL:

```bash
docker exec -it db psql -U $DB_USER -d $DB_NAME
```

Check stored data:

```sql
SELECT * FROM events;
```

---

## Stop and Clean Up

To stop containers and remove volumes:

```bash
docker compose down -v
```

---

## Notes

* The `version` field in `docker-compose.yml` is deprecated and can be safely removed.
* If Spark image issues occur, ensure the Dockerfile uses a valid Spark base image.
* Ensure `.env` file is present before running Docker Compose.