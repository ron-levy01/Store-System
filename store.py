import yaml

from errors import TooManyMatchesError, ItemNotExistError, ItemAlreadyExistsError
from item import Item
from shopping_cart import ShoppingCart


class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
        """" Arguments: the current instance of Store and an instance of str.
        Return value: a sorted list of all the items that match the search term. """

        # making candidate list of all matched items
        candidate_list = [item for item in self._items if item_name in item.name]
        return self.__sort_list(candidate_list)

    def search_by_hashtag(self, hashtag: str) -> list:
        """" Arguments: the current instance of Store and an instance of str.
        Return value: a sorted list of all the items matching the phrase. """

        candidate_list = [item for item in self._items if hashtag in item.hashtags]
        return self.__sort_list(candidate_list)

    # this function sorts as defined in the note
    def __sort_list(self, curr_list) -> list:
        """ Arguments: the current instance of Store and a list of items.
        Return value: a sorted list that does not include items which are already in the current shopping cart
        and the list is ordered in descending order by their common hashtags with the current shopping list,
        (meaning the first items will have many common hashtags with the current shopping list).
        Afterwards the sorted will be by lexicographic order off the items name"""

        # removing results that appears in current shopping cart
        for curr_item_in_shopping_list in self._shopping_cart.get_item_list():
            for item_iter in curr_list:
                if curr_item_in_shopping_list.name == item_iter.name:
                    curr_list.remove(item_iter)

        # building tags just as defined in the note
        tags = []
        for item_iter in self._shopping_cart.get_item_list():
            for hashtag in item_iter.hashtags:
                tags.append(hashtag)

        # making another list that will tell how many hashtags an element in some index has (in curr_list).
        # if hashtags [3] = 5 that means that the item in index 3 in curr_list has 5 hashtags in curr shop cart
        curr_appearing = 0
        hashtags_appearance = []
        for item_iter in curr_list:
            for hashtag in item_iter.hashtags:
                curr_appearing += tags.count(hashtag)
            hashtags_appearance.append(curr_appearing)
            curr_appearing = 0

        # sorting by hashtags and afterwards by name
        tuple_list = [(hashtags_appearance[i], curr_list[i]) for i in range(0, len(curr_list))]
        # inside sort for the name and outside sort for the hashtags
        sorted_tuple_list = sorted(sorted(tuple_list, key=lambda x: x[1].name), key=lambda x: x[0], reverse=True)
        return [item[1] for item in sorted_tuple_list]

    def add_item(self, item_name: str):
        """" Adds an item with the given name to the customer’s shopping cart.
        Arguments: the current instance of Store and an instance of str.
        Exceptions: if no such item exists, raises ItemNotExistError exception.
        If there are multiple items matching the given name, raises TooManyMatchesError exception.
        If the given item is already in the shopping cart, raises ItemAlreadyExistsError exception. """

        # making candidates list using the item name i got
        candidates_list = [item for item in self._items if item_name in item.name]

        # making candidates list of items who are in the current shopping list
        shared_candidates_list = []
        for curr_candidate in candidates_list:
            for curr_item in self._shopping_cart.get_item_list():
                if curr_candidate.name == curr_item.name:
                    shared_candidates_list.append(curr_candidate)

        if len(candidates_list) - len(shared_candidates_list) > 1:
            raise TooManyMatchesError
        if len(candidates_list) == 0:
            raise ItemNotExistError
        if len(candidates_list) == len(shared_candidates_list):
            raise ItemAlreadyExistsError

        # adding
        element_to_add = (set(candidates_list) - set(shared_candidates_list)).pop()
        self._shopping_cart.add_item(element_to_add)

    def remove_item(self, item_name: str):
        """ Removes an item with the given name from the customer’s shopping cart.
        Arguments: the current instance of Store and an instance of str.
        Exceptions: if no such item exists, raises ItemNotExistError exception .
        If there are multiple items matching the given name, raises TooManyMatchesError exception. """

        # making candidates list using the item name i got
        candidates_list = [item for item in self._items if item_name in item.name]

        # making candidates list of items who are in the current shopping list
        shared_candidates_list = []
        for curr_candidate in candidates_list:
            for curr_item in self._shopping_cart.get_item_list():
                if curr_candidate.name == curr_item.name:
                    shared_candidates_list.append(curr_candidate)

        if len(shared_candidates_list) > 1:
            raise TooManyMatchesError
        if len(shared_candidates_list) == 0:
            raise ItemNotExistError
        # removing
        self._shopping_cart.remove_item(shared_candidates_list.pop().name)

    def checkout(self) -> int:
        """" Returns the total price of all the items in the costumer’s shopping cart. """
        return self._shopping_cart.get_subtotal()
