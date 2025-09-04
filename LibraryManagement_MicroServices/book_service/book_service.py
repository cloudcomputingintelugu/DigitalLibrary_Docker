from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ujwal@2016",
        database="digital_library"
    )

@app.route("/books", methods=["GET"])
def get_books():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(books)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

