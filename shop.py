import json

avaible_items = ["life_potion", "life_mixture", "hook"]

items_for_sell = {}
for i in avaible_items:
    with open("items/"+i+".json") as d:
        data = json.load(d)
    items_for_sell[i] = data