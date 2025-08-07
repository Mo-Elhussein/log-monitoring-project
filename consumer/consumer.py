import os
import time
import psycopg2
from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "logs")

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "logsdb")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")

print(f" Kafka Broker set to: {KAFKA_BROKER}")
print(" Waiting 20 seconds for Kafka to be ready...")
time.sleep(20)

print("📡 Connecting to Kafka...")
try:
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='log-consumer-group'
    )
    print(" Connected to Kafka!")
except Exception as e:
    print(f" Failed to connect to Kafka: {e}")
    exit(1)

print("🔗 Connecting to PostgreSQL...")
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    log TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


print("Listening for new messages...")
for msg in consumer:
    log_line = msg.value.decode("utf-8")
    
    if log_line.strip() and '\x00' not in log_line:
        print(f"Inserting log: {log_line}")
        cursor.execute("INSERT INTO logs (log) VALUES (%s)", (log_line,))
        conn.commit()
    else:
        print("Skipped empty or invalid log")


