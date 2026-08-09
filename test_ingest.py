import json
import requests

with open("inbox.json", "r", encoding="utf-8") as f:
    emails = json.load(f)

payload = {
    "candidate_id": "sai.teja@gmail.com",
    "emails": emails
}

response = requests.post("http://127.0.0.1:8000/ingest", json=payload)
print(response.status_code)
print(response.json())