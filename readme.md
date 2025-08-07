Real-Time Log Processing with Kafka & PostgreSQL
This project implements a real-time pipeline to process log files using Apache Kafka and store them in a PostgreSQL database.
Tech Stack
Apache Kafka
PostgreSQL
Docker & Docker Compose
Python 3.8+
Project Components
Producer
Source: Reads log entries from logs/Apache.log.
Action: Sends each log line as a message to the logs Kafka topic.
Consumer
Source: Subscribes to the logs Kafka topic.
Action: Inserts each received log message into the logs table in PostgreSQL.
PostgreSQL Table: logs
Columns: id (SERIAL PRIMARY KEY), log (TEXT), created_at (TIMESTAMP).
Running the Project
Clone the repository:
bash
git clone https://github.com/Mo-Elhussein/log-monitoring-project.git
cd log-monitoring-project
Start the services:
This command builds and starts all containers (Kafka, Zookeeper, PostgreSQL, Producer, Consumer).
bash
docker-compose up --build -d
Verify the data:
Connect to the PostgreSQL container and query the logs table.
bash
docker-compose exec postgres psql -U admin -d logsdb -c "SELECT * FROM logs LIMIT 10;"
Stop the services:
bash
docker-compose down