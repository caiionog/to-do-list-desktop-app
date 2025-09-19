from models.Usuario import *
from models.Admin import *
from models.Tarefa import *

def run_app():
    print('Aplicativo Iniciado')
    user1 = Usuario(1, 'caio', 'caio@email')
    admin1 = Admin(1, 'caio_admin', 'caio_admin@email')
    tarefa1 = Tarefa(1, "Realizar lista de exercícios", 1)
    print(f'Usuário {user1.getId()}, Nome: {user1.getUsername()}, Email: {user1.getEmail()}')
    print(f'Admin {admin1.getId()}, Nome: {admin1.getUsername()}, Email: {admin1.getEmail()}')
    print(f'Tarefa {tarefa1.getId()}, Descrição: {tarefa1.getDescription()}, Id do Usuário Atribuido: {tarefa1.getUserId()}, Tarefa está concluída? {tarefa1.getStatus()}')

if __name__ == '__main__':
    run_app()
