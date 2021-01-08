import requests
from munch import munchify
import math
from copy import deepcopy

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

    def __lower_dict_keys(self,dict):
        result = {}
        for key, value in dict.items():
            try:
                result[key.lower()] = value
            except AttributeError:
                result[key] = value
        return result

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

    def get_crafting_steps(self,item,num_elements=1,inventory=dict()):
        def get_crafting(elemento,num_elements,inventory):
            elements_needed = self.get_craft_needed(elemento)
            element_name = self.get_exact_item(elemento).name
            try:
                item_quantity = inventory[element_name]
                inventory[element_name] -= 1
            except KeyError:
                item_quantity = 0

            if item_quantity >= num_elements:
                steps_list = []
            else:
                steps_list = [element_name]

            for element_needed in elements_needed:
                if element_needed.craftable: steps_list.extend(get_crafting(element_needed.id,num_elements,inventory))
            return steps_list

        element = self.get_exact_item(item).id
        craft_list = get_crafting(element,num_elements,deepcopy(inventory))
        craft_list.reverse()

        results = []
        #A dict that contains each element in the list and how many times it's repeated
        counter = {x:craft_list.count(x) for x in craft_list}

        for craft in counter:
            try:
                item_quantity = inventory[craft]
            except KeyError:
                item_quantity = 0

            num_elements_tmp = num_elements * counter[craft] - item_quantity

            for i in range(math.ceil(num_elements_tmp / 3)):
                if num_elements_tmp <= 3:
                    num_steps = num_elements_tmp
                else:
                    num_steps = 3
                    num_elements_tmp -= 3

                dict_craft = {craft:num_steps}
                results.append(dict_craft)

        return results

    def get_craft_total_needed_base_items(self,item,num_elements=1,inventory=dict()):
        def get_crafting(elemento):
            elements_needed = self.get_craft_needed(elemento)
            base_elements = self.get_craft_needed_base(elemento)

            for element_needed in elements_needed:
                if element_needed.craftable:
                     base_elements.extend(get_crafting(element_needed.id))

            return base_elements

        craft_list = get_crafting(self.get_exact_item(item).id)
        craft_list = {x:craft_list.count(x) for x in craft_list}
        delete_keys = list()
        for craft in craft_list:
            craft_list[craft] *= num_elements
            try:
                craft_list[craft] -= inventory[craft]
                if craft_list[craft] <= 0: delete_keys.append(craft)
            except KeyError:
                continue

        for delete in delete_keys:
            del craft_list[delete]

        return craft_list
