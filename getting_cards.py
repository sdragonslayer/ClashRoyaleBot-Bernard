import json 

with open('clash_royale_cards.json', 'r') as clash:
    data = json.load(clash)

right_cards = {}