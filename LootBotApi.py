import requests
from munch import munchify

class Error500(Exception):
    """Raised when the input value is too small"""
    pass


class LootBotApi:
    def __init__(self,token):
        self.token = token
        self.endpoint = f"http://fenixweb.net:3300/api/v2/{self.token}"

    def __request_url(self,url):
        response_json = requests.get(url).json()
        response_code = response_json["code"]
        if response_code != 200:
            raise Error500(response_json["error"])

        return munchify(response_json["res"])

    def get_items(self,rarity = None):
        if rarità != None:
            return self.get_item(rarity)

        return self.__request_url(f"{self.endpoint}/items")

    def get_item(self,item):
        return self.__request_url(f"{self.endpoint}/items/{item}")

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
        return self.__request_url(f"{self.endpoint}/crafts/{item_id}/needed")

    def get_craft_used(self,item_id):
        return self.__request_url(f"{self.endpoint}/crafts/{item_id}/used")

    def get_crafts(self):
        return self.__request_url(f"{self.endpoint}/crafts/id")
