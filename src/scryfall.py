import json
import re

import urllib.request as request
import urllib.parse as parse

from urllib.error import HTTPError

from .card import Card


class ScryFall:
    """
    A very barebone wrapper around the scryfall api.
    """

    def __init__(self):
        self.API_URL = "https://api.scryfall.com"

        # If set to true the wrapper will load every single match and not just
        # the first page of responses
        self.LOAD_ALL_MATCHES = False

    class CardLimitException(Exception):
        def __init__(self):
            self.message = "**OMG** Too many cards returned by the query, I can't handle them all. *winks*"

    class ScryfallException(Exception):
        def __init__(self, json):
            self.message = json["details"]

    def _load_url_as_json(self, url):
        """
        Load a given url into a json object.
        """
        try:
            url = request.urlopen(url)
        except HTTPError as e:
            # Try to get the ScryFall response error
            response = e.read()
            try:
                error_json = json.loads(response)
                raise self.ScryfallException(error_json)

            # Do nothing if it's a real http excepion
            except json.decoder.JSONDecodeError:
                pass

        return json.loads(url.read().decode("utf-8", "replace"))

    def get_card_rulings(self, cardid):
        url = f"{self.API_URL}/cards/{cardid}/rulings"
        rulings = self._load_url_as_json(url)
        return rulings["data"]

    def get_count(self, query):
        """Get a random card by QUERY"""

        url = self.API_URL + "/cards/search?q={}".format(parse.quote_plus(query)) + \
            "&-t:token&-layout:art_series&-t:card&\(-banned:vintage&or&t:conspiracy&or&o:ante&or&o:'one&foot'&or&Shahrazad\)"

        result = self._load_url_as_json(url)

        return result["total_cards"]

    def card_random(self, query):
        """Get a random card by QUERY"""

        url = self.API_URL + "/cards/random?q={}".format(parse.quote_plus(query)) + \
            "&-t:token&-layout:art_series&-t:card&\(-banned:vintage&or&t:conspiracy&or&o:ante&or&o:'one&foot'&or&Shahrazad\)"
        search_url = self.API_URL + "/cards/search?q={}".format(parse.quote_plus(query)) + \
            "&-t:token&-layout:art_series&-t:card&\(-banned:vintage&or&t:conspiracy&or&o:ante&or&o:'one&foot'&or&Shahrazad\)"

        result = self._load_url_as_json(url)
        count_result = self._load_url_as_json(url)

        # If we haven't found a card abort the seach
        if result["object"] == "error":
            raise self.ScryfallException(result)

        return Card(result)

    def card_named(self, name, exact=False):
        """Get a card named NAME"""

        if exact:
            url = self.API_URL + "/cards/named?exact=" + parse.quote(name)
        else:
            url = self.API_URL + "/cards/named?fuzzy=" + parse.quote(name)

        result = self._load_url_as_json(url)

        # If we haven't found a card abort the seach
        if result["object"] == "error":
            raise self.ScryfallException(result)

        return Card(result)

    def search_card(self, query, max_cards=None, order="name", alchemy=False):
        """
        Search for a card by name.
        """
        result = None
        try:
            if not ":" in query and max_cards and max_cards == 1:
                url = "{}/cards/search?order={}&q={}".format(self.API_URL,
                                                             order,
                                                             parse.quote_plus(f"!'{query}'"))
                result = self.get_cards_from_url(url, max_cards, alchemy, True)
        except ScryFall.ScryfallException:
            pass
        if not result:
            url = "{}/cards/search?order={}&q={}".format(self.API_URL,
                                                         order,
                                                         parse.quote_plus(query))
            result = self.get_cards_from_url(url, max_cards, alchemy)
        # Strip custom scryfall arguments from the cardname
        name = re.sub("[a-z]+:[a-z]+", "", query).strip().lower()
        for card in result:
            # If we have an exact match and it's not a DFC or a flip card, return just one
            if card.name.lower() == name and (
                    ("all_parts" not in card) and
                    (card.object != "card_face")):
                return [card]

        return result

    def get_cards_from_url(self, url, max_cards=None, alchemy=False, pass_error=False):
        """
        Return all cards from a given url.
        """
        cards = []
        layout_blacklist = ["art_series", "token", "double_faced_token"]
        try:
            while True:
                j = self._load_url_as_json(url)

                if j["object"] == "error" and not pass_error:
                    raise self.ScryfallException(j)

                count = j["total_cards"]

                if max_cards and count > max_cards and not pass_error:
                    raise self.CardLimitException()

                data = j["data"]
                for obj in data:

                    # Ignore Alchemy cards
                    if not alchemy and (obj["collector_number"].startswith("A-") or obj["set_type"] == "alchemy"):
                        continue

                    # Ignore the art series cards
                    if obj["layout"] in layout_blacklist:
                        continue

                    if "card_faces" in obj:
                        for face in obj["card_faces"]:
                            face["prices"] = obj["prices"]
                            face["scryfall_uri"] = obj["scryfall_uri"]
                            cards.append(Card(face))
                    else:
                        cards.append(Card(obj))

                if self.LOAD_ALL_MATCHES and j["has_more"]:
                    url = j["next_page"]
                else:
                    break

        except IOError:
            pass

        return cards
