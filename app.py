from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("webapp.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("image")

    if not file:
        return jsonify({"error": "Фото не получено"})

    # Фейковая оценка для теста
    import random
    score = random.randint(5, 10)

    return jsonify({"score": score})
