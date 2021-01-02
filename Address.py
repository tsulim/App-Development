class Address:

    def __init__(self, firstname, lastname, address, country, city, state, postalcode, mobile, currentID):
        currentID += 1
        self.__firstname = firstname
        self.__lastname = lastname
        self.__addressID = currentID
        self.__address = address
        self.__country = country
        self.__city = city
        self.__state = state
        self.__postalcode = postalcode
        self.__mobile = mobile

    def get_firstname(self):
        return self.__firstname

    def get_lastname(self):
        return self.__lastname

    def get_addressID(self):
        return self.__addressID

    def get_address(self):
        return self.__address

    def get_country(self):
        return self.__country

    def get_city(self):
        return self.__city

    def get_state(self):
        return self.__state

    def get_postalcode(self):
        return self.__postalcode

    def get_mobile(self):
        return self.__mobile

    def set_firstname(self,firstname):
        self.__firstname = firstname

    def set_lastname(self,lastname):
        self.__lastname = lastname

    def set_addressID(self,addressID):
        self.__addressID = addressID

    def set_address(self,address):
        self.__address = address

    def set_country(self,country):
        self.__country = country

    def set_city(self,city):
        self.__city = city

    def set_state(self,state):
        self.__state = state

    def set_postalcode(self,postalcode):
        self.__postalcode = postalcode

    def set_mobile(self, mobile):
        self.__mobile = mobile
