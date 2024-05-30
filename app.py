from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)


DB_CONFIG = {
    'user': 'postgres',
    'password': 'Rakesh062',
    'host': 'localhost',
    'database': 'postgres'
}

# Create the database table if it doesn't exist
def init_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL,
                            subject VARCHAR(255) NOT NULL,
                            message TEXT NOT NULL)''')
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                       (name, email, subject, message))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    except mysql.connector.Error as err:
        return jsonify(success=False, error=str(err))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
