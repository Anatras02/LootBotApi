import requests
from munch import munchify
import math
import json
from pathlib import Path

class Error500(Exception):
    pass


class LootBotApi:
    def __init__(self,token):
        self.token = token
        self.endpoint = f"http://fenixweb.net:3300/api/v2/{self.token}"
        self.items = self.get_items()
        self.craft_needed = dict()

    def __request_url(self,url):
        response_json = requests.get(url).json()
        response_code = response_json["code"]
        if response_code != 200:
            raise Error500(response_json["error"])

        return munchify(response_json["res"])

    def get_items(self,rarity = None):
        if rarity != None:
            return self.get_item(rarity)

        return self.__request_url(f"{self.endpoint}/items")

    def get_item(self,item):
        item_return = list(filter(lambda item_search: item_search.name == item, self.items))
        if item_return == []:
            item_return = list(filter(lambda item_search: item_search.rarity == item, self.items))
            if item_return == []:
                item_return = self.__request_url(f"{self.endpoint}/items/{item}")
        return item_return

    def get_exact_item(self,item):
        item_api = self.get_item(item)
        if type(item_api) is list:
            for sub_item in item_api:
                if sub_item.name == item:
                    return sub_item
        else:
            return item_api

    def get_history(self,place = "payments",limit = None,offset = None,fromPlayer = None,toPlayer = None,fromItem = None,toItem = None,both = None,fromPrice = None,toPrice = None,orderBy = "desc"):
        string = f"{self.endpoint}/history/{place}?"
        arguments = locals()
        """
        The paramater to cannot be called from because it's a python key and so we changed it to "toPlayer" but we have to change it back to "to" for the request
        This process can probably be done in a better way.
        """
        arguments["to"] = arguments.pop("toPlayer")
        arguments["from"] = arguments.pop("fromPlayer")

        for argument in arguments:
            if argument in ["self","string"]:
                continue
            else:
                if arguments[argument] != None:
                    string += f"{argument}={arguments[argument]}&"


        string = string[:-1]
        return self.__request_url(string)

    def get_players(self):
        return self.__request_url(f"{self.endpoint}/players")

    def get_player(self,player):
        return self.__request_url(f"{self.endpoint}/players/{player}")[0]

    def get_team(self,team):
        return self.__request_url(f"{self.endpoint}/team/{team}")

    def get_searches(self,quantity):
        return self.__request_url(f"{self.endpoint}/search/{quantity}")

    def get_cards(self):
        return self.__request_url(f"{self.endpoint}/cards")

    def get_info(self):
        return self.__request_url(f"{self.endpoint}/info")

    def get_global(self):
        return self.__request_url(f"{self.endpoint}/global")

    def get_shop(self,shop):
        return self.__request_url(f"{self.endpoint}/shop/{shop}")

    def get_craft_needed(self,item_id):
        try:
            craft_needed = self.craft_needed[item_id]
        except KeyError:
            craft_needed = self.__request_url(f"{self.endpoint}/crafts/{item_id}/needed")
            self.craft_needed[item_id] = craft_needed

        return craft_needed

    def get_craft_needed_base(self,item_id):
        craft_needed = self.get_craft_needed(item_id)
        return list(filter(lambda item : not item.craftable,craft_needed))

    def get_craft_used(self,item_id):
        return self.__request_url(f"{self.endpoint}/crafts/{item_id}/used")

    def get_crafts(self):
        return self.__request_url(f"{self.endpoint}/crafts/id")

    def get_total_craft_points(self,item):
        item = self.get_exact_item(item)
        return item.craft_pnt

    def get_average_market_price(self,item):
        item = self.get_exact_item(item)

        item_name = item.name
        item_base_price = item.value
        prezzi = self.get_history(place="market_direct",fromItem=item_name,fromPrice=item_base_price+1)
        return int(sum(prezzo.price for prezzo in prezzi) / len(prezzi))

    def get_crafting_steps(self,item,num_elements=1):
        def get_crafting(elemento):
            elements_needed = self.get_craft_needed(elemento)
            steps_list = [self.get_item(elemento).name]
            for element_needed in elements_needed:
                if element_needed.craftable: steps_list.extend(get_crafting(element_needed.id))
            return steps_list

        element = self.get_exact_item(item).id
        craft_list = get_crafting(element)
        craft_list.reverse()

        results = []
        #A dict that contains each element in the list and how many times it's repeated
        counter = {x:craft_list.count(x) for x in craft_list}

        for craft in counter:
            try:
                inventory_count = inventory[craft.lower()]
            except KeyError:
                inventory_count = 0

            num_elements_tmp = (num_elements * counter[craft]) - inventory_count

            for i in range(math.ceil(num_elements_tmp / 3)):
                if num_elements_tmp <= 3:
                    num_steps = num_elements_tmp
                else:
                    num_steps = 3
                    num_elements_tmp -= 3

                dict_craft = {craft:num_steps}
                results.append(dict_craft)

        return results

    def get_craft_total_needed_base_items(self,item,num_elements=1):
        def get_crafting(elemento):
            elements_needed = self.get_craft_needed(elemento)
            base_elements = [base.name for base in self.get_craft_needed_base(elemento)]

            for element_needed in elements_needed:
                if element_needed.craftable:
                     base_elements.extend(get_crafting(element_needed.id))
            return base_elements

        craft_list = get_crafting(self.get_exact_item(item).id)
        craft_list = {x:craft_list.count(x) for x in craft_list}
        if num_elements != 1:
            for craft in craft_list:
                craft_list[craft] *= num_elements
        return craft_list
