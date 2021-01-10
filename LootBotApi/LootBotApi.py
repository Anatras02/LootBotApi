import requests
from munch import munchify
import math
from copy import deepcopy
import pathlib
import json

class Error500(Exception):
    pass


class LootBotApi:
    def __init__(self,token):
        self.token = token
        self.endpoint = f"http://fenixweb.net:3300/api/v2/{self.token}"
        self.items = self.get_items()
        self.craft_needed = self.__load_json("craft_needed.json")
        self.INVENTORY_SYNTAX_ERROR = "The inventory should be in the format {'element':quantity}"

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

    def __get_path(self,name):
        HERE = pathlib.Path(__file__).parent
        return f"{HERE}/{name}"

    def __save_dict(self,name,dict):
        HERE = pathlib.Path(__file__).parent
        with open(self.__get_path(name), 'w') as fp:
            json.dump(dict, fp)

    def __load_json(self,name):
        path = self.__get_path(name)
        if pathlib.Path(path).is_file():
            with open(path) as json_file:
                return json.load(json_file)
        else:
            new_dict = dict()
            f = open(path, 'a+')
            f.write("{}")
            f.close()
            #self.__save_dict(path,new_dict)
            return new_dict

    def get_items(self,rarity = None):
        if rarity != None:
            return self.get_item(rarity)

        return self.__request_url(f"{self.endpoint}/items")

    def get_item(self,item):
        item_return = list(filter(lambda item_search: item_search.name == item, self.items))
        if item_return == []:
            item_return = list(filter(lambda item_search: item_search.id == item, self.items))
            if item_return == []:
                item_return = list(filter(lambda item_search: item_search.rarity == item, self.items))
                if item_return == []:
                    item_return = self.__request_url(f"{self.endpoint}/items/{item}")
        return item_return

    def get_exact_item(self,item):
        item_api = self.get_item(item)
        if type(item_api) is list:
            for sub_item in item_api:
                if sub_item.name == item or sub_item.id == item:
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
            self.__save_dict("craft_needed.json",self.craft_needed)

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
        def get_crafting(element,inventory):
            elements_needed = self.get_craft_needed(element)
            element_name = self.get_exact_item(element).name
            try:
                element_name_tmp = element_name.lower()
                try:
                    inventory[element_name_tmp] = int(inventory[element_name_tmp])
                    item_quantity = inventory[element_name_tmp]
                    inventory[element_name_tmp] -= 1
                    if inventory[element_name_tmp] == 0: del inventory[element_name_tmp]
                except ValueError:
                    raise SyntaxError(INVENTORY_SYNTAX_ERROR)
            except KeyError as e:
                item_quantity = 0

            if item_quantity >= 1:
                 return []
            else:
                elements_needed = list(filter(lambda x: x.craftable,elements_needed))
                steps_list = {element_name:[]}
                for element_needed in elements_needed:
                    crafts = get_crafting(element_needed.id,inventory)
                    if crafts != []: steps_list[element_name].append(crafts)
                return steps_list

        def get_steps(craft_list):
            steps_list = list()
            for craft_tree in craft_list:
                if craft_tree == []: continue
                key = list(craft_tree.keys())[0]
                steps_list.append(key)
                steps_list.extend(get_steps(craft_tree[key]))

            return steps_list


        inventory = self.__lower_dict_keys(inventory)
        element = self.get_exact_item(item).id
        craft_list = list()

        for i in range(0,num_elements):
            craft_list.append(get_crafting(element,inventory))

        craft_list = get_steps(craft_list)
        craft_list.reverse()

        results = []
        #A dict that contains each element in the list and how many times it's repeated
        counter = {x:craft_list.count(x) for x in craft_list}
        for craft in counter:
            try:
                item_quantity = int(inventory[craft.lower()])
            except KeyError:
                item_quantity = 0

            num_elements_tmp = counter[craft]

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
        steps = self.get_crafting_steps(item,num_elements,inventory)
        base_list = list()
        base_dict = dict()
        inventory = self.__lower_dict_keys(inventory)

        for step in steps:
            for item in step:
                item_api = self.get_exact_item(item)
                base_step_list = self.get_craft_needed(item_api.id)
                base_step_list = list(filter(lambda x: not x.craftable,base_step_list))
                base_step_list = [base_item.name for base_item in base_step_list]
                base_list.extend(base_step_list*step[item])

        for x in base_list:
            try:
                inventory_count = int(inventory[x.lower()])
            except KeyError:
                inventory_count = 0
            base_dict[x] = base_list.count(x) - inventory_count
            if base_dict[x] <= 0: del base_dict[x]

        return base_dict
