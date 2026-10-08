import json
import time
from pathlib import Path

DATA_FILE = Path(__file__).parent / "merged_items.json"

TAX_RATE = 0.02
TAX_CAP = 5_000_000


def calculate_tax(sell_price, tax_exempt=False):
    if tax_exempt:
        return 0

    return min(int(sell_price * TAX_RATE), TAX_CAP)


def analyze_flip(
    item_name: str,
    max_age_minutes: int = 1440,
    tax_exempt: bool = False
) -> dict:

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    now = time.time()

    for item_id, item in dataset["items"].items():

        if item["name"].casefold() != item_name.strip().casefold():
            continue

        buy_price = item.get("low")
        sell_price = item.get("high")
        high_time = item.get("highTime")
        low_time = item.get("lowTime")

        if any(v is None for v in (
            buy_price, sell_price, high_time, low_time
        )):
            return {
                "item": item_name,
                "error": "Missing price or timestamp data"
            }

        high_age = (now - high_time) / 60
        low_age = (now - low_time) / 60

        if high_age < 0 or low_age < 0:
            return {
                "item": item_name,
                "error": "Price timestamps are in the future"
            }

        if max(high_age, low_age) > max_age_minutes:
            return {
                "item": item_name,
                "error": "Price observations are too old",
                "high_age_minutes": round(high_age, 1),
                "low_age_minutes": round(low_age, 1)
            }

        tax = calculate_tax(sell_price, tax_exempt)
        gross_profit = sell_price - buy_price
        net_profit = gross_profit - tax

        roi = (
            net_profit / buy_price * 100
            if buy_price > 0 else None
        )

        return {
            "id": int(item_id),
            "name": item["name"],
            "suggested_buy_price": buy_price,
            "suggested_sell_price": sell_price,
            "estimated_tax": tax,
            "gross_margin": gross_profit,
            "estimated_net_profit": net_profit,
            "estimated_roi_percent": (
                round(roi, 2) if roi is not None else None
            ),
            "profitable_on_paper": net_profit > 0,
            "high_age_minutes": round(high_age, 1),
            "low_age_minutes": round(low_age, 1),
            "fetchedAt": dataset["fetchedAt"],
            "warning": (
                "Indicative prices based on previous trades. "
                "Orders may not fill at these prices. "
                "Tax exemptions must be verified."
            )
        }

    return {"error": f"Item '{item_name}' not found"}


if __name__ == "__main__":
    print(json.dumps(
        analyze_flip("Abyssal whip"),
        indent=2
    ))