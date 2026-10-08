from price_tools import get_item_price
from flipping_tools import analyze_flip

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_item_price",
            "description": (
                "Look up the recorded Grand Exchange high and low "
                "prices for an Old School RuneScape item by name."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": (
                            "The OSRS item name, such as "
                            "'Abyssal whip' or 'Mirror shield'."
                        )
                    }
                },
                "required": ["item_name"]
            }
        }
    }
]

AVAILABLE_FUNCTIONS = {
    "get_item_price": get_item_price
}

FLIP_TOOL = {
    "type": "function",
    "function": {
        "name": "analyze_flip",
        "description": (
            "Analyze the potential Grand Exchange flipping "
            "margin, tax, ROI and price freshness for an OSRS item."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "Exact OSRS item name"
                }
            },
            "required": ["item_name"]
        }
    }
}

TOOLS.append(FLIP_TOOL)

AVAILABLE_FUNCTIONS["analyze_flip"] = analyze_flip