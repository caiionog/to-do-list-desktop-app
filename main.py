from services.UserManager import UserManager
from services.TaskManager import TaskManager
from services.AuthController import AuthController
from interface.Menu import Interface
from interface.App import App

def run_app():
    print('Aplicativo Iniciado')
    user_manager = UserManager()
    task_manager = TaskManager()
    auth_controller = AuthController(user_manager)
    admin1 = user_manager.addUser('admin', 'admin@email', True)
    app = App(auth_controller, user_manager, task_manager) 
    app.mainloop()

if __name__ == '__main__':
    run_app()
