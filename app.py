from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("webapp.html")

if name == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
