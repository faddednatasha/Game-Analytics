import json
import requests

# Your master API key
API_KEY = "bq4KZzSQTYxZz6PIPFsqREw05thmMBZZCcMCN6rY"

# Endpoint: Competitions by Category (ATP)
URL = "https://api.sportradar.com/tennis/trial/v3/en/categories/sr%3Acategory%3A3/competitions.json"

headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

print("Fetching ATP category competitions...")
response = requests.get(URL, headers=headers, timeout=10)

if response.status_code == 200:
    data = response.json()
    print(f"Success! Retrieved {len(data.get('competitions', []))} competitions.")
    
    # Save the JSON response to a local file
    with open("atp_competitions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Saved output to 'atp_competitions.json'")

else:
    print(f"Error {response.status_code}: {response.text}")