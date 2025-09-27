from models.Tarefa import Tarefa

class TaskManager:
    def __init__(self):
        self._all_tasks = []
        self._next_task_id = 1

    def addTask(self, description, userId):
        new_task = Tarefa(self._next_task_id, description, userId)
        self._all_tasks.append(new_task)
        self._next_task_id += 1 
        return new_task
    
    def markTaskCompleted(self, taskId, userId):
        for task in self._all_tasks:
            if task.getId() == taskId and task.getUserId() == userId:
                task.completeTask()
                return True
        return False
    
    def deleteTask(self, taskId, userId):
        for task in self._all_tasks:
            if task.getId() == taskId and task.getUserId() == userId:
                self._all_tasks.remove(task)
                return True
        return False
    
    def addTaskEveryone(self, description, user_manager):
        for user in user_manager.getAllUsers():
            self.addTask(description, user.getId())
    
    def getTasksForUser(self, userId):
        tasks = [task for task in self._all_tasks if task.getUserId() == userId]
        return tasks