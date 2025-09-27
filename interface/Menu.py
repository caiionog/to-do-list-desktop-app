class Interface:
    def __init__(self, user_manager, task_manager, auth_controller):
        self.user_manager = user_manager
        self.task_manager = task_manager
        self.auth_controller = auth_controller
        self.current_user = None

    def login_menu(self):
        print("\n--- Menu de Login ---")
        print("1. Fazer Login")
        print("0. Sair do Aplicativo")
        escolha = input('Digite uma opção: ')
        if escolha == '1':
            id = int(input('Digite seu ID: '))
            user = self.auth_controller.login(id)
            if user:
                self.current_user = user
                print(f"Login bem-sucedido! Bem-vindo, {user.getUsername()}.")
            else:
                print("ID inválido. Tente novamente.")
        elif escolha == '0':
            print("Saindo do aplicativo...")
            exit()
        else:
            print("Opção inválida. Tente novamente.")

    def user_menu(self):
        print("\n--- Menu ---")
        print("1. Criar Nova Tarefa")
        print("2. Gerenciar Minhas Tarefas")
        print("3. Logout")
        print("4. Menu Admin" if self.current_user.isAdmin() else "------------")
        print("0. Sair do Aplicativo")
        escolha = input('Digite uma opção: ')
        if escolha == '1':
            description = input('Descrição da Tarefa: ')
            self.task_manager.addTask(description, self.current_user.getId())
            print("Tarefa criada com sucesso!")
        elif escolha == '2':
            self.current_user.viewTask(self.task_manager)
            task_id = int(input('Digite o ID da tarefa para modificar ela (ou 0 para voltar): '))
            if task_id != 0:
                print('1. Deletar Tarefa')
                print('2. Marcar como Concluída')
                action = input('Escolha uma ação: ')
                if action == '1':
                    if self.task_manager.deleteTask(task_id, self.current_user.getId()):
                        print("Tarefa deletada com sucesso!")
                    else:
                        print("ID de tarefa inválido ou não pertence a você.")
                elif action == '2':
                    if self.task_manager.markTaskCompleted(task_id, self.current_user.getId()):
                        print("Tarefa marcada como concluída!")
                    else:
                        print("ID de tarefa inválido ou não pertence a você.")
        elif escolha == '3':
            self.current_user = None
            print("Logout realizado com sucesso.")
        elif escolha == '4' and self.current_user.isAdmin():
            self.admin_menu()
        elif escolha == '0':
            print("Saindo do aplicativo...")
            exit()
        else:
            print("Opção inválida. Tente novamente.")

    def admin_menu(self):
        print("\n--- Menu Admin ---")
        print("1. Criar Novo Usuário")
        print("2. Criar Tarefa para Usuário")
        print("3. Criar Tarefa para Todos os Usuários")
        print("4. Excluir Usuário")
        print("5. Gerenciar Tarefas de Usuário")
        print("0. Voltar ao Menu Principal")
        escolha = input('Digite uma opção: ')
        if escolha == '1':
            username = input('Nome de Usuário: ')
            email = input('Email: ')
            admin = input('É Admin? (s/n): ').lower() 
            if admin == 's':
                new_user = self.user_manager.addUser(username, email, True)
            elif admin == 'n':
                new_user = self.user_manager.addUser(username, email, False)
            else:
                print("Entrada inválida para admin. Usuário não criado.")
                return
            print(f"Usuário criado com sucesso! ID do usuário: {new_user.getId()}")
        elif escolha == '2':
            user_id = int(input('ID do Usuário: '))
            description = input('Descrição da Tarefa: ')
            user = self.user_manager.getUserById(user_id)
            if user:
                self.task_manager.addTask(description, user_id)
                print("Tarefa criada com sucesso para o usuário!")
            else:
                print("ID de usuário inválido.")
        elif escolha == '3':
            description = input('Descrição da Tarefa para Todos: ')
            self.task_manager.addTaskEveryone(description, self.user_manager)
            print("Tarefa criada com sucesso para todos os usuários!")
        elif escolha == '4':
            user_id = int(input('ID do Usuário a ser Excluído: '))
            if user_id == self.current_user.getId():
                print("Você não pode excluir a si mesmo.")
                return
            user = self.user_manager.getUserById(user_id)
            if user:
                self.user_manager._all_users.remove(user)
                print("Usuário excluído com sucesso.")
            else:
                print("ID de usuário inválido.")
        elif escolha == '5':
            user_id = int(input('ID do Usuário para Gerenciar Tarefas: '))
            user = self.user_manager.getUserById(user_id)
            if user:
                user.viewTask(self.task_manager)
                task_id = int(input('Digite o ID da tarefa para modificar ela (ou 0 para voltar): '))
                if task_id != 0:
                    print('1. Deletar Tarefa')
                    print('2. Marcar como Concluída')
                    action = input('Escolha uma ação: ')
                    if action == '1':
                        if self.task_manager.deleteTask(task_id, user_id):
                            print("Tarefa deletada com sucesso!")
                        else:
                            print("ID de tarefa inválido ou não pertence ao usuário.")
                    elif action == '2':
                        if self.task_manager.markTaskCompleted(task_id, user_id):
                            print("Tarefa marcada como concluída!")
                        else:
                            print("ID de tarefa inválido ou não pertence ao usuário.")
            else:
                print("ID de usuário inválido.")
        elif escolha == '0':
            return
        else:
            print("Opção inválida. Tente novamente.")
        
    def run(self):
        while True:           
            if self.current_user:
                self.user_menu()
            else:
                self.login_menu()
