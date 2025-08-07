import os
import time
from kafka import KafkaProducer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "logs")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/app/logs/Apache.log")

print(f" Kafka Broker set to: {KAFKA_BROKER}")
print(" Waiting 20 seconds for Kafka to be ready...")
time.sleep(20)

try:
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    print("Connected to Kafka!")
except Exception as e:
    print(f" Failed to connect to Kafka: {e}")
    exit(1)

def follow_log():
    last_size = 0
    while True:
        try:
            with open(LOG_FILE_PATH, "r") as f:
                f.seek(last_size)
                lines = f.readlines()
                if lines:
                    for line in lines:
                        line = line.strip()
                        if line:
                            print(f" Sending log: {line}")
                            producer.send(TOPIC_NAME, value=line.encode("utf-8"))
                last_size = f.tell()
        except Exception as e:
            print(f"Error reading log file: {e}")
        time.sleep(1)

if __name__ == "__main__":
    follow_log()
