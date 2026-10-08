import requests
import json
from datetime import datetime, timezone

url = "https://prices.runescape.wiki/api/v1/osrs"

headers = {
    "User-Agent": "price_predictor - @{discord username}"
}
def get_prices():
    response = requests.get(
        f"{url}/latest",
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    prices = response.json()["data"]

    fetched_at = int(datetime.now(timezone.utc).timestamp())

    data = {
        "fetchedAt": fetched_at,
        "prices": prices
    }

    with open("osrs_prices.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Collected prices for {len(prices)} items")

def get_id_names():
    response = requests.get(
    f"{url}/mapping",
    headers=headers,
    timeout=30
    )
    response.raise_for_status()

    items = response.json()

    id_to_name = {
        str(item["id"]): item["name"]
        for item in items
    }

    with open("item_mapping.json", "w") as f:
        json.dump(id_to_name, f, indent=2)

    print(id_to_name.get("4151"))
    # Abyssal whip

def merge_data():
    with open("osrs_prices.json", "r") as f:
        price_data = json.load(f)

    with open("item_mapping.json", "r") as f:
        names = json.load(f)

    # Extract prices and fetch timestamp
    prices = price_data["prices"]
    fetched_at = price_data["fetchedAt"]

    merged = {}

    for item_id, data in prices.items():
        merged[item_id] = {
            "name": names.get(item_id, "Unknown"),
            **data
        }

    # Preserve fetchedAt at the top level
    merged_data = {
        "fetchedAt": fetched_at,
        "items": merged
    }

    with open("merged_items.json", "w") as f:
        json.dump(merged_data, f, indent=2)

    print(f"Merged {len(merged)} items!")
    print(f"Fetched at: {fetched_at}")

if __name__ == "__main__":
    get_prices()
    get_id_names()
    merge_data()