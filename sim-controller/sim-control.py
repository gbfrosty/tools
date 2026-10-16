import csv
import json
import sys
import keyboard
from playwright.sync_api import sync_playwright

state = {
    "url": "https://wos-sim.ratme.org/simualate-wosui",
    "rally_mode": True,
    "player1": "FrostyBest",
    "player2": "AlphaAtk",
}

def run_simulation():
    try:
        # Load and validate CSV and JSON configuration before launching Playwright
        selectors = load_json_selectors("selectors.json")
        data = load_csv_data("battle_stats.csv", state["player1"], state["player2"])
        validate_data(data, state["player1"], state["player2"])
        
    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f"[Data Error] {e}")
        sys.exit(1)

    with sync_playwright() as p:
        # Connect to existing Chrome instance running with --remote-debugging-port=9222
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # Get or create active page
        default_context = browser.contexts[0]
        page = default_context.pages[0] if default_context.pages else default_context.new_page()
        
        # Navigate to simulator
        page.goto(state["url"])
        
        # Perform inputs
        populate_sim(page, selectors, data)
        
        #input("Press Enter to finish and exit...")

def load_json_selectors(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_csv_data(filepath, player1, player2):
    data = {"attacker": {}, "defender": {}}
    
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            player = row["Player"].strip()
            troop_type = row["Troop_Type"].strip().lower()

            # Map player1 directly to attacker, regardless of the 'Side' column in CSV
            if player == player1:
                data["attacker"][troop_type] = {
                    "tier": row["Tier"].strip().lower() + "_" + row["Camp"].strip().lower(),
                    "count": row["Troops"].strip(),
                    "atk": row["Atk"].strip(),
                    "def": row["Def"].strip(),
                    "leth": row["Leth"].strip(),
                    "hp": row["Hp"].strip()
                }
            # Map player2 directly to defender
            elif player == player2:
                data["defender"][troop_type] = {
                    "tier": row["Tier"].strip().lower() + "_" + row["Camp"].strip().lower(),
                    "count": row["Troops"].strip(),
                    "atk": row["Atk"].strip(),
                    "def": row["Def"].strip(),
                    "leth": row["Leth"].strip(),
                    "hp": row["Hp"].strip()
                }
    return data

def validate_data(data, player1, player2):
    """Ensures both players exist in the parsed dictionary."""
    missing = []
    
    if not data["attacker"]:
        missing.append(f"Player 1 ('{player1}') was not found in the CSV file.")
    if not data["defender"]:
        missing.append(f"Player 2 ('{player2}') was not found in the CSV file.")

    if missing:
        raise ValueError("\n".join(missing))

def populate_sim(page, selectors, data):
    if not state["rally_mode"]:
        page.uncheck("input[name='simulate.syncHeroStats']")

    for side in ["attacker", "defender"]:
        side_data = data[side]
        side_selectors = selectors[side]

        for troop_type, stats in side_data.items():
            if troop_type not in side_selectors:
                print(f"[Warning] No selector found for troop type '{troop_type}' on side '{side}'. Skipping.")
                continue

            troop_selectors = side_selectors[troop_type]
            stats_selectors = troop_selectors["stats"]

            page.select_option(f"select[name='{troop_selectors['tier']}']", value=stats["tier"])

            # Input fields by name attribute: input[name='...']
            page.fill(f"input[name='{troop_selectors['count']}']", stats["count"])
            page.fill(f"input[name='{stats_selectors['atk']}']", stats["atk"])
            page.fill(f"input[name='{stats_selectors['def']}']", stats["def"])
            page.fill(f"input[name='{stats_selectors['leth']}']", stats["leth"])
            page.fill(f"input[name='{stats_selectors['hp']}']", stats["hp"])

    print(f"Loaded Attacker ({state['player1']}) and Defender ({state['player2']}).")
    #print("Script finished. Browser will remain open.")

def main():
    state["player1"] = input("Enter player 1 name ")
    state["player2"] = input("Enter player 2 name ")
    
    rally_mode = input("Rally Mode y/n ")
    state["rally_mode"] = True if rally_mode.lower() == 'y' else False
    
    url = input("Url [optional] ")
    if url: state["url"] = url

    run_simulation()

    # Block thread until 'esc' is pressed
    #keyboard.wait('esc')
    #print("Exiting...")

if __name__ == "__main__":
    main()