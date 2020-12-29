# LootBotApi
This is an API wrapper for Loot Bot (https://telegra.ph/Guida-alle-LootBot-API-04-06)

# Guide
1. Clone the repository and put it in your code directory
2. Import the library
`from LootBotApi import LootBotApi`
3. Create the object `api = LootBotApi(TOKEN)` --> the token can be found using the command /token on https://t.me/lootplusbot
4. Call the methods from the object created above

# Methods
All the attributes of this methods can be accesed either as dict keys or object attributes.

## Items
* `get_items(rarity = None)` It returns all the items in the game, if rarity is passed it returns all the items of that rarity
* `get_item(item)` It returns the info about a given item
```
print(api.get_item("Meccanismo di Ferro").id) #363
print(api.get_item(363).name) #Meccanismo di Ferro
```
## History
* `get_history(place = "payments",limit = None,offset = None,fromPlayer = None,toPlayer = None,fromItem = None,toItem = None,both = None,fromPrice = None,toPrice = None,orderBy = "desc")` It returns the transactions with the specificied parameters

## Players
* `get_players()` It returns all the players of LootBot
* `get_player(player)` It returns the info about the player

## Crafting 
* `get_crafts()` It returns all the crafts in the game
* `get_craft_needed(item_id)` It returns the items requested to craft the item
* `get_craft_used(item_id)` It returns the item that you can craft using the item
```
items = api.get_craft_needed(363)
for item in items:
  print(item.name)
  
#Perno
#Meccanismo di Legno
#Ferro
```

## Shops
* `get_shop(shop)` It returns the infos about the shop

## Cards
* `get_crafts()` It returns all the cards in the game

## Global
* `get_global()` It returns the progress of the current global challenge, it's updated every hour
* `get_info()` It returns infos about the current global challenge

## Team
* `get_team(team)` it returns the infos about a team

## Ricerche
* `get_searches(quantity)` It returns the searches made on the bot
