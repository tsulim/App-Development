from datetime import datetime

class Order:
    def __init__(self, orderDict, currentID):
        currentID += 1
        self.__orderID = currentID

        self.__date = datetime.now().strftime('%x')
        self.__time = datetime.now().strftime('%X')
        self.__orderdict = orderDict
        self.__paymentmethod = ""
        self.__address = ""
        self.__overall_cost = 0
        self.__orderStatus = ""
        self.__deliveryID = ""
        self.__userID = ""

    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_orderdict(self, orderDict):
        self.__orderdict = orderDict

    def set_date(self):
        self.__date = datetime.now().strftime('%x')

    def set_time(self):
        self.__time = datetime.now().strftime('%X')

    def set_paymentmethod(self,paymentmethod):
        self.__paymentmethod = paymentmethod

    def set_address(self,address):
        self.__address = address

    def set_overall_cost(self, overall):
        self.__overall_cost = overall

    def set_orderStatus(self, orderStatus):
        self.__orderStatus = orderStatus

    def set_deliveryID(self,deliveryID):
        self.__deliveryID = deliveryID

    def set_userID(self,userID):
        self.__userID = userID

    def get_orderID(self):
        return self.__orderID

    def get_orderdict(self):
        return self.__orderdict

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_paymentmethod(self):
        return self.__paymentmethod

    def get_address(self):
        return self.__address

    def get_overall_cost(self):
        # self.__overall_cost = 0
        # for book in self.__orderdict:
        #     quantity = self.__orderdict[book][2]
        #     price = self.__orderdict[book][1]
        #     total_cost = price * quantity
        #     self.__overall_cost += total_cost

        return self.__overall_cost

    def get_orderStatus(self):
        return self.__orderStatus

    def get_deliveryID(self):
        return self.__deliveryID

    def get_userID(self):
        return self.__userID

# def add_book_order(order, title, quantity, price):
#     bookdict = order.get_orderdict()
#     bookdict[title] = [quantity,price]
#
#     order.set_bookdict(bookdict)
#
# def del_book_order(order, title):
#     bookdict = order.get_orderdict()
#     bookdict.pop(title)
#
#     order.set_bookdict(bookdict)
#
# def modify_book_order(order, title, quantity):
#     bookdict = order.get_orderdict()
#     bookdict[title] = [quantity, bookdict[title][1]]
#
#     order.set_bookdict(bookdict)

def get_total_cost(order, title):
    quantity = order.get_orderdict()[title][0]
    price = order.get_orderdict()[title][1]
    total_cost = price * quantity
    return total_cost

# test codes
# o = Order()
#
# add_book_order(o, 'blehh', 2, 2.5)
# add_book_order(o, 'uhhhh', 4, 4)
#
# del_book_order(o, 'blehh')
#
# modify_book_order(o, 'uhhhh', 3)
#
#
# print(o.get_date())
# print(o.get_time())
# print(o.get_orderID(), o.get_bookdict())
#
# o = Order()
#
# print(o.get_date())
# print(o.get_time())
# print(o.get_orderID(),o.get_bookdict())
#
