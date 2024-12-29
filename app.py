from flask import Flask, request, jsonify, make_response
# from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HEADERS = {"Authorization": f"Bearer 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"}

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    if data and 'text' in data:
        text = data['text']
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": text})
        result = response.json()
        flask_response = make_response(jsonify(result))
        flask_response.headers.add("Access-Control-Allow-Origin", "*")
        flask_response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        flask_response.headers.add("Access-Control-Allow-Methods", "POST")
        return flask_response
    else:
        return make_response(jsonify({"error": "Invalid input"}), 400)

if __name__ == '__main__':
    app.run(debug=True)
