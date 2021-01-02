class User:
    def __init__(self, firstName, lastName, topic, question):
        self.__firstName = firstName
        self.__lastName = lastName
        self.__topic = topic
        self.__question = question
        self.__ans = ''
        self.__key = question
        self.__counter = [0]

    def get_firstName(self):
        return self.__firstName
    def get_lastName(self):
        return self.__lastName
    def get_topic(self):
        return self.__topic
    def get_question(self):
        return self.__question
    def get_ans(self):
        return self.__ans
    def get_key(self):
        return self.__key
    def get_counter(self):
        return self.__counter

    def set_firstName(self, firstName):
        self.__firstName = firstName
    def set_lastName(self, lastName):
        self.__lastName = lastName
    def set_topic(self, topic):
        self.__topic = topic
    def set_question(self, question):
        self.__question = question
    def set_ans(self, ans):
        self.__ans = ans
    def set_counter(self, counter):
        self.__counter = counter
