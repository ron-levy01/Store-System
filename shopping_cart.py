from errors import ItemNotExistError, ItemAlreadyExistsError, TooManyMatchesError
from item import Item


class ShoppingCart:

    def __init__(self):
        self._item_list = []

    def get_item_list(self):
        """" Returns the item list of the current shopping cart instance. """
        return self._item_list

    def add_item(self, item: Item):
        """" Adds the given item to the current shopping cart.
        Arguments: the current instance of ShoppingCart and an instance of Item.
        Exceptions: if the item already exists in the shopping cart, raises ItemAlreadyExistsError exception."""

        for item_iter in self._item_list:
            if item_iter.name == item.name:
                raise ItemAlreadyExistsError
        self._item_list.append(item)

    def remove_item(self, item_name: str):
        """" Removes the item with the given name from the shopping cart.
        Arguments: the current instance of ShoppingCart and an instance of str.
        Exceptions: if no item with the given name exists, raises ItemNotExistError exception ."""

        removed = False
        for item_iter in self._item_list:
            if item_iter.name == item_name:
                self._item_list.remove(item_iter)
                removed = True
        if not removed:
            raise ItemNotExistError

    def get_subtotal(self) -> int:
        """" Returns the subtotal price of all the items currently in the shopping cart. """

        total_price = 0
        for item_iter in self._item_list:
            total_price += item_iter.price
        return total_price
