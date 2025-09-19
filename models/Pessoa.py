from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, id, username, email):
        self._id = id
        self._username = username
        self._email = email

    def getUsername(self):
        return f'{self._username}'

    def getEmail(self):
        return f'{self._email}'

    def getId(self):
        return self._id

    def setUsername(self, x):
        self._username = x

    def setEmail(self, x):
        self._email = x

    def setId(self, x):
        self._id = x

    def viewTask(self):
        pass
    
