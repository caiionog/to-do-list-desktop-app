from models.Tarefa import Tarefa
from models.TarefaRepository import TarefaRepository

class TaskManager:
    def __init__(self):
        self.model = TarefaRepository('taskDB.db')

    def addTask(self, description, userId):
        new_task = Tarefa(description, userId) 
        self.model.adicionar_tarefa(new_task.getUserId(), new_task.getDescription().strip()) 
        return new_task
    
    def markTaskCompleted(self, taskId, userId):
        for task in self._all_tasks:
            if task.getId() == taskId and task.getUserId() == userId:
                description = task.getDescription()
                self.model.atualizar_tarefa(taskId, userId, description, True)
                return True
        return False
    
    def deleteTask(self, taskId, userId):
        self.model.excluir_tarefa(taskId, userId)
    
    def addTaskEveryone(self, description, user_manager):
        for user in user_manager.getAllUsers():
            self.addTask(description, user.getId())
    
    def getTasksForUser(self, userId):
        tasks = [task for task in self._all_tasks if task.getUserId() == userId]
        return tasks
