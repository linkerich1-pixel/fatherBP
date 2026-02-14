from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

@app.route("/")
def home():
    return send_file("webapp.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["image"]
    image = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return jsonify({"error": "Лицо не найдено"})

    score = min(10, max(1, len(faces) * 7))

    return jsonify({"score": score})
