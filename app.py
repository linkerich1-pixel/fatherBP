from flask import Flask, request, jsonify
import cv2
import numpy as np
import mediapipe as mp

app = Flask(__name__)

mp_face_mesh = mp.solutions.face_mesh

def analyze_face(image):
    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            return {"error": "Лицо не найдено"}

        landmarks = results.multi_face_landmarks[0]

        h, w, _ = image.shape
        points = []

        for lm in landmarks.landmark:
            x, y = int(lm.x * w), int(lm.y * h)
            points.append((x, y))

        # Пример простой оценки симметрии
        left_eye = points[33]
        right_eye = points[263]

        eye_distance = abs(left_eye[0] - right_eye[0])
        face_width = abs(points[234][0] - points[454][0])

        symmetry_score = 10 - abs(eye_distance - face_width / 3) / 10

        final_score = max(1, min(10, round(symmetry_score, 2)))

        return {
            "score": final_score,
            "details": {
                "eye_distance": eye_distance,
                "face_width": face_width
            }
        }

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["image"]
    image = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    result = analyze_face(image)
    return jsonify(result)

@app.route("/")
def home():
    return "Face Analyzer API is running"

if __name__ == "__main__":
    app.run(debug=True)

