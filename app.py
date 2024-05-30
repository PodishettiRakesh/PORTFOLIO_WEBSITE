from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql, OperationalError

app = Flask(__name__)

# Replace these with your actual PostgreSQL database credentials
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Rakesh062',
    'host': 'localhost',
    'port': '5432'
}

# Create the database table if it doesn't exist
def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                subject VARCHAR(255) NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except OperationalError as e:
        print(f"Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            sql.SQL("INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)"),
            [name, email, subject, message]
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    except OperationalError as e:
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
