from flask import Flask, render_template, request
import cv2
import numpy as np
import mediapipe as mp
import math
import os

app = Flask(__name__)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# золотое сечение
PHI = 1.618


def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


def golden_ratio_score(ratio):
    return 1 - abs(ratio - PHI)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['image']
    if not file:
        return "No file uploaded"

    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        return "Invalid image"

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return "Face not found"

    landmarks = results.multi_face_landmarks[0].landmark

    # ключевые точки
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    chin = landmarks[152]
    forehead = landmarks[10]
    left_cheek = landmarks[234]
    right_cheek = landmarks[454]
    nose_tip = landmarks[1]

    # расстояния
    face_height = distance(forehead, chin)
    face_width = distance(left_cheek, right_cheek)
    eye_distance = distance(left_eye, right_eye)

    # соотношения
    ratio1 = face_height / face_width
    ratio2 = face_height / eye_distance

    score1 = golden_ratio_score(ratio1)
    score2 = golden_ratio_score(ratio2)

    # симметрия
    mid_x = (left_cheek.x + right_cheek.x) / 2
    symmetry = 1 - abs(nose_tip.x - mid_x)

    # итог
    final_score = (score1 + score2 + symmetry) / 3
    final_score = max(0, min(final_score * 10, 10))
    final_score = round(final_score, 2)

    return f"""
    <h2>Your Face Score: {final_score} / 10</h2>
    <p>Golden Ratio 1: {round(score1,3)}</p>
    <p>Golden Ratio 2: {round(score2,3)}</p>
    <p>Symmetry: {round(symmetry,3)}</p>
    <br>
    <a href="/">Try Again</a>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

