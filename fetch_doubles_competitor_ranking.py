import json
import requests

# API Configuration
API_KEY = "bq4KZzSQTYxZz6PIPFsqREw05thmMBZZCcMCN6rY"
URL = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"

headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

print("Fetching doubles competitor rankings...")
response = requests.get(URL, headers=headers, timeout=10)

if response.status_code == 200:
    data = response.json()
    rankings = data.get("rankings", [])
    print(f"Success! Retrieved {len(rankings)} ranking groups.\n")

    # Save raw JSON to file
    with open("doubles_competitor_rankings.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Saved raw output to 'doubles_competitor_rankings.json'\n")

    # Preview top rankings for each league group (e.g., ATP / WTA doubles)
    for group in rankings:
        group_name = group.get("name", "N/A")
        group_type = group.get("type_id", "")
        competitor_rankings = group.get("competitor_rankings", [])
        
        print(f"--- {group_name} Doubles Rankings (Top 5) ---")
        print(f"{'RANK':<6} | {'POINTS':<8} | {'PLAYER NAME':<30} | {'COUNTRY':<8}")
        print("-" * 60)
        
        for item in competitor_rankings[:5]:
            rank = item.get("rank", "N/A")
            points = item.get("points", "N/A")
            player = item.get("competitor", {})
            p_name = player.get("name", "N/A")
            p_country = player.get("country_code", "N/A")
            print(f"{rank:<6} | {points:<8} | {p_name:<30} | {p_country:<8}")
        print("\n")

else:
    print(f"Error {response.status_code}: {response.text}")