import requests
url = "http://localhost:8000/query"
payload = {"query": "what are your qualifcations"}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.json())