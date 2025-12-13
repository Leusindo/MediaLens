from flask import Flask, request, jsonify
from flask_cors import CORS
from core.classifier import NewsClassifier

app = Flask(__name__)
CORS(app)  # povolí CORS pre všetky originy (na demo ideálne)

classifier = NewsClassifier()
# podľa tvojho projektu buď load, alebo init, podľa toho čo máš:
# classifier.load_models()

@app.route("/classify", methods=["POST", "OPTIONS"])
def classify():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Empty text"}), 400

    result = classifier.classify(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
