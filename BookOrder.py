class BookOrder:

    def __init__(self, title, price, quantity, image):
        self.__title = title
        self.__price = float(price)
        self.__quantity = int(quantity)
        self.__image = image

    def set_orderbkID(self, orderbkID):
        self.__orderbkID = orderbkID

    def get_orderbkID(self):
        return self.__orderbkID

    def set_title(self,title):
        self.__title = title

    def get_title(self):
        return self.__title

    def set_price(self,price):
        self.__price = float(price)

    def get_price(self):
        return self.__price

    def set_quantity(self,quantity):
        self.__quantity = int(quantity)

    def get_quantity(self):
        return self.__quantity

    def set_image(self, image):
        self.__image = image

    def get_image(self):
        return self.__image

    def get_total_cost(self):
        return self.__price * self.__quantity
