from flask import Flask, jsonify
from waitress import serve
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import uuid
import logging

app = Flask(__name__)

# Load environment variables
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'mydatabase')
db_user = os.getenv('DB_USER', 'myuser')
db_pass = os.getenv('DB_PASS', 'mypassword')

def init_db():
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id SERIAL PRIMARY KEY,
            data TEXT NOT NULL
        );
    """)

    cur.close()
    conn.close()

@app.route('/')
def add_entry():
    # Insert random data
    random_data = str(uuid.uuid4())
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()
    cur.execute("INSERT INTO entries (data) VALUES (%s) RETURNING id;", (random_data,))
    entry_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # Logger
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.log(logging.INFO, "This is a standard log message using the log method")

    return jsonify(
        message="This is a simple, basic Python application running on Zerops.io, each request adds an entry to the PostgreSQL database and returns a count. See the source repository (https://github.com/zeropsio/recipe-python) for more information.",
        id=entry_id,
        data=random_data
    )

@app.route('/status')
def status_check():
    return jsonify(status="UP")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)

    # Example of using WSGI server for production
    # serve(app, host="0.0.0.0", port=8000)