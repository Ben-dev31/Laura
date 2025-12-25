import requests

SERVER_URL = "http://127.0.0.1:5001/transcribe"

if __name__ == '__main__':
    r = requests.post(SERVER_URL, json={"text": "Bonjour, ceci est un test"})
    print(r.status_code, r.text)
