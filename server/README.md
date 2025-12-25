# Simple Transcription Server

This Flask server accepts POST requests at `/transcribe` with JSON `{ "text": "..." }` and returns `{ "reply": "..." }`.

Run the server:

```bash
python server/simple_server.py
```

It listens by default on port 5001.

The client (in `client/client.py`) will send transcriptions to `http://127.0.0.1:5001/transcribe` and display or speak replies.
