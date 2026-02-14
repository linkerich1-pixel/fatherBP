from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running"

@app.route("/webapp")
def webapp():
    return render_template("webapp.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    return jsonify({
        "score": 7.8,
        "advice": "Good base. Improve hairstyle and reduce face fat."
    })

if name == "__main__":
    app.run(host="0.0.0.0", port=10000)