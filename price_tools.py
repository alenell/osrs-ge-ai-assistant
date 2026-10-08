import json
from pathlib import Path
from datetime import datetime, timezone

DATA_FILE = Path(__file__).parent / "merged_items.json"


def format_time(timestamp):
    if timestamp is None:
        return None

    return datetime.fromtimestamp(
        timestamp, tz=timezone.utc
    ).isoformat()


def get_item_price(item_name: str) -> dict:
    """Retrieve an OSRS item's prices from cached API data."""

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    items = dataset["items"]
    fetched_at = dataset["fetchedAt"]

    for item_id, item in items.items():
        if item["name"].casefold() == item_name.strip().casefold():
            return {
                "id": int(item_id),
                "name": item["name"],
                "high": item.get("high"),
                "low": item.get("low"),
                "highTime": format_time(item.get("highTime")),
                "lowTime": format_time(item.get("lowTime")),
                "fetchedAt": format_time(fetched_at)
            }

    return {"error": f"Item '{item_name}' not found"}


if __name__ == "__main__":
    print(get_item_price("Mirror shield"))