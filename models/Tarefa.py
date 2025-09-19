class Tarefa:
    def __init__(self, id, description, userId):
        self._id = id
        self._description = description
        self._userId = userId
        self._isCompleted = False

    def completeTask(self):
        self._isCompleted = true
        
    def assignToUser(self, id):
        self._userId = id

    def getId(self):
        return self._id

    def getDescription(self):
        return f'{self._description}'

    def getUserId(self):
        return self._userId

    def getStatus(self):
        return self._isCompleted
