# LootBotApi
This is an API wrapper for Loot Bot (https://telegra.ph/Guida-alle-LootBot-API-04-06)

# Installation
## Download from PyPi
1. `pip install LootBotApi`
2. `from LootBotApi import LootBotApi`
3. `api = LootBotApi(TOKEN)` --> the token can be found using the command /token on https://t.me/lootplusbot
4. Call the methods from the object created above


# Methods
## Api Wrapper
Most of this methods will return a list of Munch objects.
This means that the attributes of the result can either be accessed as dictionary keys or object attributes
### Items
* `get_items(rarity = None)` It returns all the items in the game, if rarity is passed it returns all the items of that rarity
* `get_item(item)` It returns the info about a given item
``` python
print(api.get_item("Meccanismo di Ferro").id) #363
print(api.get_item(363).name) #Meccanismo di Ferro
```
### History
* `get_history(place = "payments",limit = None,offset = None,fromPlayer = None,toPlayer = None,fromItem = None,toItem = None,both = None,fromPrice = None,toPrice = None,orderBy = "desc")` It returns the transactions with the specificied parameters

### Players
* `get_players()` It returns all the players of LootBot
* `get_player(player)` It returns the info about the player

### Crafting
* `get_crafts()` It returns all the crafts in the game
* `get_craft_needed(item_id)` It returns the items requested to craft the item
* `get_craft_used(item_id)` It returns the item that you can craft using the item
``` python
items = api.get_craft_needed(363)
for item in items:
  print(item.name)

#Perno
#Meccanismo di Legno
#Ferro
```

### Shops
* `get_shop(shop)` It returns the infos about the shop

### Cards
* `get_crafts()` It returns all the cards in the game

### Global
* `get_global()` It returns the progress of the current global challenge, it's updated every hour
* `get_info()` It returns infos about the current global challenge

### Team
* `get_team(team)` it returns the infos about a team

### Ricerche
* `get_searches(quantity)` It returns the searches made on the bot

## Custom Methods
These methods are not natively implemented in the API but they are derived by them.

### Crafting
* `get_total_craft_points(item)` It returns the total craft points that you will get to craft the item
``` python
 print(api.get_total_craft_points("Ordigno Polverizzatore")) #113
```
* `get_crafting_steps(item,num_elements=1)` It returns as a list of dicts all the steps to craft a certain element (and in a certain quantity)
``` python
steps = api.get_crafting_steps("Scudo Punta Doppia",5)
for step in steps:
    for elemento in step:
        print(f"Crea {elemento},{step[elemento]}")
"""
Crea Scudo Punta Singola,3
Crea Scudo Punta Singola,2
Crea Scudo Punta Doppia,3
Crea Scudo Punta Doppia,2
"""
```

### Market
* `get_average_market_price(item)` It returns the average price of an item in the market as an integer
``` python
 print(api.get_average_market_price("Ferro")) #37394
```

### Items
* `get_exact_item(item)` It returns the exact item searched
``` python
print(api.get_element("Carta"))
"""
[Munch({'id': 1, 'name': 'Carta', 'rarity': 'C', 'rarity_name': 'Comuni', 'value': 410, 'max_value': 205000, 'estimate': 2000, 'spread': 46, 'spread_tot': 0.116, 'craftable': 0, 'reborn': 1, 'power': 0, 'power_armor': 0, 'power_shield': 0, 'dragon_power': 0, 'critical': 0, 'craft_pnt': 0, 'cons_val': 0}), Munch({'id': 8, 'name': 'Carta Stropicciata', 'rarity': 'NC', 'rarity_name': 'Non Comuni', 'value': 810, 'max_value': 405000, 'estimate': 1237, 'spread': 44, 'spread_tot': 0.084, 'craftable': 0, 'reborn': 1, 'power': 0, 'power_armor': 0, 'power_shield': 0, 'dragon_power': 0, 'critical': 0, 'craft_pnt': 0, 'cons_val': 0}), Munch({'id': 35, 'name': 'Aereo di Carta Piccolo', 'rarity': 'NC', 'rarity_name': 'Non Comuni', 'value': 1121, 'max_value': 1121000, 'estimate': 11750, 'spread': 30, 'spread_tot': 0.001, 'craftable': 1, 'reborn': 1, 'power': 0, 'power_armor': 0, 'power_shield': 0, 'dragon_power': 0, 'critical': 0, 'craft_pnt': 0, 'cons_val': 0.1}), Munch({'id': 36, 'name': 'Aereo di Carta Grande', 'rarity': 'R', 'rarity_name': 'Rari', 'value': 1697, 'max_value': 1697000, 'estimate': 13045, 'spread': 28, 'spread_tot': 0.001, 'craftable': 1, 'reborn': 1, 'power': 0, 'power_armor': 0, 'power_shield': 0, 'dragon_power': 0, 'critical': 0, 'craft_pnt': 1, 'cons_val': 0.15}), Munch({'id': 37, 'name': 'Caccia di Carta', 'rarity': 'UR', 'rarity_name': 'Ultra Rari', 'value': 3468, 'max_value': 3468000, 'estimate': 4650, 'spread': 25, 'spread_tot': 0, 'craftable': 1, 'reborn': 1, 'power': 0, 'power_armor': 0, 'power_shield': 0, 'dragon_power': 0, 'critical': 0, 'craft_pnt': 3, 'cons_val': 0.25})]
"""

print(api.get_exact_item("Carta"))
"""
Munch({'id': 1, 'name': 'Carta', 'rarity': 'C', 'rarity_name': 'Comuni', 'value': 410, 'max_value': 205000, 'estimate': 2000, 'spread': 46, 'spread_tot': 0.116, 'craftable': 0, 'reborn': 1, 'power': 0, 'power_armor': 0, 'power_shield': 0, 'dragon_power': 0, 'critical': 0, 'craft_pnt': 0, 'cons_val': 0})
"""
```
