class objDelivery:
    def __init__(self, deliveryID, statusDict):
        self.__deliveryID = deliveryID
        self.__statusDict = statusDict

    def set_deliveryID(self, deliveryID):
        self.__deliveryID = deliveryID

    def get_deliveryID(self):
        return self.__deliveryID

    def set_statusDict(self, statusDict):
        self.__statusDict = statusDict

    def get_statusDict(self):
        return self.__statusDict
