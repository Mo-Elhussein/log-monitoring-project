CREATE TABLE IF NOT EXISTS log_metrics (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    operation_type VARCHAR(10),
    status_code INT,
    count INT
);
