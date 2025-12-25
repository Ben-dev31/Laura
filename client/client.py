from flask import Flask, jsonify
from flask import request

import threading
import time
import requests
import logging

from inputsystem import AudioInput
from outputsystem import OutputSystem

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
SERVER_URL = "http://127.0.0.1:5001/server"  # server to send transcriptions to

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok"}), 200

@app.route('/listen', methods=['POST'])
def listen_and_respond():
    """Manual trigger: listen once, send transcription and return server reply."""
    try:
        text = audio_input.listen()
    except Exception as e:
        logging.exception("Error during listening")
        return jsonify({"error": str(e)}), 500

    if not text:
        return jsonify({"error": "no speech recognized"}), 400

    try:
        resp = requests.post(SERVER_URL, json={"text": text}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        reply = data.get('reply', '')
        output_system.out(reply)
        return jsonify({"transcript": text, "reply": reply}), 200
    except Exception as e:
        logging.exception("Error sending to server")
        return jsonify({"error": str(e)}), 500


def background_listener(stop_event: threading.Event):
    """Continuously listen, send transcript to server, and display reply."""
    logging.info("Background listener started")
    while not stop_event.is_set():
        try:
            text = audio_input.listen(timeout=3, phrase_time_limit=10)
        except Exception as e:
            logging.exception("Listening failure")
            time.sleep(1)
            continue

        if not text:
            # nothing recognized in this cycle
            continue

        logging.info("Recognized: %s", text)

        try:
            resp = requests.post(SERVER_URL, json={"text": text}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            reply = data.get('reply', '')
            logging.info("Server reply: %s", reply)
            output_system.out(reply)
        except Exception as e:
            logging.exception("Failed to send transcription to server")

        # short pause between phrases
        time.sleep(0.5)


def initialize_systems():
    audio_input = AudioInput()
    output_system = OutputSystem(outtype='console')  # use console output by default
    return audio_input, output_system


audio_input, output_system = initialize_systems()

if __name__ == '__main__':
    stop_event = threading.Event()
    listener_thread = threading.Thread(target=background_listener, args=(stop_event,), daemon=True)
    listener_thread.start()

    try:
        # Run Flask app (this is a simple example; in production use waitress/gunicorn)
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        logging.info("Shutting down")
    finally:
        stop_event.set()
        listener_thread.join(timeout=2)
        logging.info("Exited")
