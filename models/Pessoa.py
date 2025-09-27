from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, id, username, email, isAdmin):
        self._id = id
        self._username = username
        self._email = email
        self._is_admin = isAdmin

    def getUsername(self):
        return self._username

    def getEmail(self):
        return self._email

    def getId(self):
        return self._id

    def setUsername(self, x):
        self._username = x

    def setEmail(self, x):
        self._email = x

    def setId(self, x):
        self._id = x

    def isAdmin(self):
        return self._is_admin

    def viewTask(self, task_manager):
        tasks = task_manager.getTasksForUser(self.getId())
        if not tasks:
            print("Nenhuma tarefa atribuída.")
        else:
            for task in tasks:
                status = "Concluída" if task.getStatus() else "Pendente"
                print(f"ID: {task.getId()} | Status: {status} | Descrição: {task.getDescription()}")
    
