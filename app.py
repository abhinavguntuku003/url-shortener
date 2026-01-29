from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import sqlite3, random, string

app = Flask(__name__)
CORS(app)

# DB init
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        long_url TEXT,
        short_code TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()

init_db()

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# API to shorten URL
@app.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.json
    long_url = data["long_url"]
    code = generate_code()

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, code))
    conn.commit()
    conn.close()
# ngrok url for Mobile QR code scanning
    # BASE_URL = "https://feigned-leda-nonhomogeneously.ngrok-free.dev/"
    short_url = request.host_url + code
    return jsonify({"short_url": short_url})

# Redirect
@app.route("/<code>")
def redirect_url(code):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_code=?", (code,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
