import json 

with open('troops.json', 'r') as clash:
    data = json.load(clash)

troops = data["troops"]

sckeys_to_find = [
    "Minions",
    "Archers",
    "Knight",
    "MiniPekka",
    "Musketeer",
    "Giant",
    "Spear Goblins",
    "Goblins"
]

filtered_troops = [troop for troop in troops if troop.get("sc_key") in sckeys_to_find]

with open('spells.json', 'r') as clash1:
    data1 = json.load(clash1)

spells = data1["spells"]

spells_to_find = [
    "Fireball",
    "Arrows"
]

filtered_spells = [spell for spell in spells if spell.get("sc_key") in spells_to_find]

with open('towertroops.json', 'r') as clash2:
    data2 = json.load(clash2)

towers = data2["tower_troops"]

filtered_towers = [tower for tower in towers if tower["arena"] <= 1]

low_arena_cards = {
    "troops": filtered_troops,
    "spells": filtered_spells,
    "towers": filtered_towers
}

with open("cards.json", "w") as new:
    json.dump(low_arena_cards, new, indent=4)