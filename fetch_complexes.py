import json
import requests

# API Configuration
API_KEY = "bq4KZzSQTYxZz6PIPFsqREw05thmMBZZCcMCN6rY"
URL = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"

headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

print("Fetching tennis complexes...")
response = requests.get(URL, headers=headers, timeout=10)

if response.status_code == 200:
    data = response.json()
    complexes = data.get("complexes", [])
    print(f"Success! Retrieved {len(complexes)} complexes.\n")

    # Save raw JSON to file
    with open("complexes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Saved raw output to 'complexes.json'\n")

    # Display preview of first 10 complexes
    print(f"{'COMPLEX ID':<25} | {'NAME':<35}")
    print("-" * 65)
    for item in complexes[:10]:
        c_id = item.get("id", "N/A")
        c_name = item.get("name", "N/A")
        print(f"{c_id:<25} | {c_name:<35}")

else:
    print(f"Error {response.status_code}: {response.text}")