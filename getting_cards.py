import json 

with open('clash_royale_cards_full.json', 'r') as clash:
    data = json.load(clash)

cards = data["cards"]

filtered = [card for card in cards if card["arena"] <= 1]

low_arena_cards = {"cards": filtered}

with open("cards.json", "w") as new:
    json.dump(low_arena_cards, new, indent=4)