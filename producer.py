import json
import random
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

pages = ["/home", "/about", "/products", "/contact"]
users = ["user_A", "user_B", "user_C"]

while True:
    event = {
        "event_time": (datetime.utcnow() - timedelta(
            minutes=random.choice([0, 0, 0, 3])
        )).isoformat(),
        "user_id": random.choice(users),
        "page_url": random.choice(pages),
        "event_type": random.choice(
            ["page_view", "click", "session_start", "session_end"]
        )
    }

    producer.send("user_activity", event)
    print("Sent:", event)
    time.sleep(1)
