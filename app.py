from flask import Flask, request, render_template
import cv2
import numpy as np

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

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

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "Face not found"

    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]

    # --- 1. Пропорция лица (высота / ширина)
    face_ratio = h / w
    ideal_ratio = 1.5
    ratio_score = max(0, 10 - abs(face_ratio - ideal_ratio) * 20)

    # --- 2. Правило третей (верх / середина / низ)
    third = h // 3
    top = face[0:third, :]
    middle = face[third:2*third, :]
    bottom = face[2*third:h, :]

    top_mean = np.mean(top)
    middle_mean = np.mean(middle)
    bottom_mean = np.mean(bottom)

    thirds_balance = abs(top_mean - bottom_mean)
    thirds_score = max(0, 10 - thirds_balance / 10)

    # --- 3. Симметрия
    left = face[:, :w//2]
    right = face[:, w//2:]
    right_flipped = cv2.flip(right, 1)

    min_width = min(left.shape[1], right_flipped.shape[1])
    left = left[:, :min_width]
    right_flipped = right_flipped[:, :min_width]

    symmetry_diff = np.mean(cv2.absdiff(left, right_flipped))
    symmetry_score = max(0, 10 - symmetry_diff / 10)

    # --- Общая оценка
    final_score = (ratio_score + thirds_score + symmetry_score) / 3
    final_score = round(final_score, 2)

    return f"""
    <h2>Your facial analysis</h2>
    Ratio score: {round(ratio_score,2)}<br>
    Thirds balance: {round(thirds_score,2)}<br>
    Symmetry: {round(symmetry_score,2)}<br><br>
    <strong>Final score: {final_score}/10</strong>
    """

if name == "__main__":
    app.run(host="0.0.0.0", port=10000)
