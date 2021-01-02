class Book:

    def __init__(self, bookName, author, price, genre, stock, summary, image, currentID):
        currentID += 1
        self.__bookID = currentID
        self.__bookName = bookName
        self.__author = author
        self.__price = float(price)
        self.__genre = genre
        self.__stock = stock
        self.__summary = summary
        self.__image = image
        self.__quantitysold = 0

    def get_bookID(self):
        return self.__bookID

    def get_bookName(self):
        return self.__bookName

    def get_author(self):
        return self.__author

    def get_price(self):
        return self.__price

    def get_genre(self):
        return self.__genre

    def get_stock(self):
        return self.__stock

    def get_summary(self):
        return self.__summary

    def get_image(self):
        return self.__image

    def get_quantitysold(self):
        return self.__quantitysold

    def set_bookID(self,bookID):
        self.__bookID = bookID

    def set_bookName(self,bookName):
        self.__bookName = bookName

    def set_author(self,author):
        self.__author = author

    def set_price(self,price):
        self.__price = float(price)

    def set_genre(self,genre):
        self.__genre = genre

    def set_stock(self,stock):
        self.__stock = stock

    def set_summary(self,summary):
        self.__summary = summary

    def set_image(self,image):
        self.__image = image

    def set_quantitysold(self,quantitysold):
        self.__quantitysold = quantitysold
