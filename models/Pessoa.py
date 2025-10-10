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
    # O TaskManager retorna uma lista de dicionários!
    # Nota: Assumindo que o nome do método é getTasksForUser, conforme seu código.
        tasks = task_manager.getTasksForUser(self.getId())
    
    # ⚠️ CORREÇÃO CRUCIAL PARA TKINTER:
    # 1. REMOVE os comandos 'print'.
    # 2. SE NÃO HOUVER TAREFAS, DEVE RETORNAR UMA LISTA VAZIA ([]) em vez de 'None'.
    
        if not tasks:
        # Se 'tasks' for uma lista vazia, retorna a própria lista vazia.
            return []
        else:
        # Se houver tarefas, retorna a lista de dicionários.
            return tasks
