from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/server', methods=['POST'])
def transcribe():
    data = request.get_json(force=True)
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'no text received'}), 400

    # Simple processing: echo + simple canned response logic
    if 'bonjour' in text.lower():
        reply = "Bonjour! Je suis le serveur. Comment puis-je vous aider?"
    elif 'au revoir' in text.lower() or 'bye' in text.lower():
        reply = "Au revoir! À bientôt."
    else:
        reply = f"Reçu: {text}"

    return jsonify({'reply': reply}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
