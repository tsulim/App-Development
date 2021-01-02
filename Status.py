from datetime import datetime

class Status:
    def __init__(self, status, currentID):
        currentID += 1
        self.__statusID = currentID

        self.__date = datetime.now().strftime('%x')
        self.__time = datetime.now().strftime('%X')
        self.__status = status

    def set_statusID(self, statusID):
        self.__statusID = statusID

    def set_status(self, status):
        self.__status = status

    def set_date(self):
        self.__date = datetime.now().strftime('%x')

    def set_time(self):
        self.__time = datetime.now().strftime('%X')

    def get_statusID(self):
        return self.__statusID

    def get_status(self):
        return self.__status

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time
