# OSRS Grand Exchange AI Assistant

A local AI assistant for Old School RuneScape (OSRS) Grand Exchange prices and flipping. It runs [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) with Hugging Face Transformers and Python function calling, so price answers come from real market data instead of the model's memory.

Ask things like *"What's the price of an Abyssal whip?"* or *"Is a Mirror shield worth flipping?"* and the model calls a tool, reads the result, and answers using only what the tool returned.

> **Disclaimer:** This is a hobby project. It is not affiliated with or endorsed by Jagex or the OSRS Wiki. Old School RuneScape is a trademark of Jagex Ltd. Nothing here is financial advice. Prices are indicative only, and orders may not fill at the suggested prices.

## Features

- **Price lookup**: recorded high/low Grand Exchange prices by item name, with trade timestamps and the time the data was fetched.
- **Flip analysis**: buy/sell margin, GE tax (2%, capped at 5M gp), net profit, ROI, and a staleness check that refuses to analyze old observations.
- **Tool-calling loop**: the model decides when to call tools, and results are fed back for a grounded answer (up to 3 tool calls per question).
- **Guardrailed system prompt**: tells the model never to invent prices, to mention data freshness, and never to promise profit.

## How it works

```
retrieve_data.py ──► osrs_prices.json ─┐
 (OSRS Wiki API)     item_mapping.json ─┴─► merged_items.json
                                                   │
                      price_tools.py  ◄────────────┤
                      flipping_tools.py ◄──────────┘
                              ▲
                          tools.py  (tool schemas + function registry)
                              ▲
                          model.py  (Qwen3-8B chat loop)
```

## Project structure

| File | Purpose |
|---|---|
| `retrieve_data.py` | Fetches the latest prices and the item ID→name mapping from the OSRS Wiki API, then merges them into `merged_items.json`. |
| `price_tools.py` | `get_item_price`: looks up an item's high/low prices and timestamps. |
| `flipping_tools.py` | `analyze_flip`: computes margin, tax, ROI, and data age. |
| `tools.py` | Tool schemas passed to the model and the name→function registry. |
| `model.py` | Loads Qwen3-8B, holds the system prompt, parses tool calls, and runs the interactive chat loop. |
| `requirements.txt` | Python dependencies. |

## Requirements

- Python 3.10+ (developed on 3.13)
- A GPU with roughly 16 GB of VRAM for Qwen3-8B in bf16 (CPU works but is very slow)
- About 16 GB of disk space for the model download

## Setup

```bash
git clone https://github.com/alenell/osrs-ge-ai-assistant.git
cd osrs-ge-ai-assistant

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The price data files are generated, not stored in the repo, so fetch them before first use:

```bash
python retrieve_data.py
```

This creates `osrs_prices.json`, `item_mapping.json`, and `merged_items.json`. Re-run it whenever you want fresher prices. The assistant reads from this cached snapshot and does not call the API live.

**Model cache location (optional):** by default Hugging Face stores the model in its standard cache folder. To use a different drive or folder, set `HF_HUB_CACHE` before running:

```bash
export HF_HUB_CACHE=/path/to/cache        # Windows (PowerShell): $env:HF_HUB_CACHE = "D:\huggingface\hub"
```

## Usage

### Chat assistant

```bash
python model.py
```

```
OSRS Grand Exchange AI
Type 'exit' to quit.

You: Is an abyssal whip worth flipping?

[Tool call] analyze_flip({'item_name': 'Abyssal whip'})
[Tool result] {'id': 4151, 'name': 'Abyssal whip', 'suggested_buy_price': 817035, 'suggested_sell_price': 823283, 'estimated_tax': 16465, 'gross_margin': 6248, 'estimated_net_profit': -10217, 'estimated_roi_percent': -1.25, 'profitable_on_paper': False, 'high_age_minutes': 10.7, 'low_age_minutes': 11.8, 'fetchedAt': 1791499574, 'warning': 'Indicative prices based on previous trades. Orders may not fill at these prices. Tax exemptions must be verified.'}


Assistant: Based on the latest analysis, flipping an Abyssal whip is not currently profitable. Here's a summary:

- **Suggested Buy Price**: 817,035 GP  
- **Suggested Sell Price**: 823,283 GP  
- **Estimated Tax**: 16,465 GP  
- **Estimated Net Profit**: -10,217 GP (a loss)  
- **Estimated ROI**: -1.25%  

The prices are indicative based on previous trades, and orders may not fill at these prices. Additionally, tax exemptions must be verified. It's not currently worth flipping an Abyssal whip.
```

The first run downloads the model, which takes a while.

### Run the tools directly

```bash
python price_tools.py        # price lookup demo (Mirror shield)
python flipping_tools.py     # flip analysis demo (Abyssal whip)
```

## Notes and limitations

- Prices are a cached snapshot. The assistant reports when the data was fetched, and `analyze_flip` rejects observations older than 24 hours by default.
- High/low values are the most recent observed trades, not guaranteed executable prices.
- Item lookup is an exact, case-insensitive name match.
- Tax exemptions for specific items are not tracked. `analyze_flip` accepts `tax_exempt=True` in code.
- Responses are generated greedily with a 400-token cap.

## Data sources and credits

- Price data: [OSRS Wiki real-time prices API](https://prices.runescape.wiki/)
- Model: [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) by the Qwen team (Apache 2.0)

The Wiki API requires a descriptive `User-Agent`. Update the value in `retrieve_data.py` to identify your own project.

## License

MIT. See [LICENSE](LICENSE).
