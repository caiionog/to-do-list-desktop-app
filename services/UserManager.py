# services/UserManager.py

from models.Pessoa import Pessoa # Importa a classe de entidade
from models.UserRepository import UserRepository # Importa o novo Model/Repository
from typing import List, Tuple, Optional 

class UserManager:
    """
    Gerenciador (Controller/Service) que usa o UserRepository para CRUD,
    mantendo a interface de funções original.
    """
    
    def __init__(self):
        # Removemos _all_users e _next_user_id
        # Instanciamos o novo Model/Repository
        self.repo = UserRepository('taskDB.db') 

    def addUser(self, username: str, email: str, isAdmin: bool) -> Optional[Pessoa]:
        """
        Adiciona um novo usuário ao banco de dados e retorna o objeto Pessoa.
        """
        # 1. Chama o Repository para inserir no BD e obter o novo ID
        new_id = self.repo.adicionar_usuario(username, email, isAdmin)
        
        if new_id is not None:
            # 2. Usa o novo ID para criar e retornar a instância da classe Pessoa
            new_user = Pessoa(new_id, username, email, isAdmin)
            return new_user
        
        # Retorna None se a inserção falhar (ex: nome de usuário duplicado)
        return None 

    def getUserById(self, userId: int) -> Optional[Pessoa]:
        """
        Busca um usuário no banco de dados pelo ID e retorna o objeto Pessoa.
        """
        # 1. Chama o Repository para buscar a tupla
        user_tuple = self.repo.buscar_usuario_por_id(userId)
        
        if user_tuple:
            # A tupla do Model é: (id, nome_usuario, email, is_admin)
            user_id, username, email, is_admin_int = user_tuple
            is_admin = is_admin_int == 1
            
            # 2. Instancia e retorna a classe Pessoa
            return Pessoa(user_id, username, email, is_admin)
            
        return None

    def getAllUsers(self) -> List[Pessoa]:
        """
        Retorna todos os usuários do banco de dados como objetos Pessoa.
        """
        # 1. Chama o Repository para obter a lista de tuplas
        users_raw = self.repo.buscar_todos_usuarios()
        
        # 2. Mapeia as tuplas para objetos Pessoa
        all_users = []
        for user_id, username, email, is_admin_int in users_raw:
            is_admin = is_admin_int == 1
            all_users.append(Pessoa(user_id, username, email, is_admin))
            
        return all_users
    
    def deleteUser(self, user: Pessoa) -> bool:
        """
        Deleta um usuário do banco de dados usando seu ID.
        Recebe o objeto Pessoa para fácil acesso ao ID.
        Retorna True se o usuário foi deletado, False caso contrário.
        """
        user_id = user.getId()
        
        # 1. VALIDAÇÃO ADICIONAL: Garante que estamos tentando deletar um ID válido
        if user_id is None or user_id <= 0:
            print(f"Tentativa de deletar usuário com ID inválido: {user_id}")
            return False
            
        # 2. Chama o Repository para executar a exclusão
        # Assumimos que o UserRepository tem o método deletar_usuario(user_id)
        success = self.repo.deletar_usuario(user_id)
        
        if success:
            print(f"Usuário ID {user_id} ({user.getUsername()}) deletado com sucesso.")
            # ⚠️ NOTA IMPORTANTE: Em um sistema completo, você precisaria
            # garantir que todas as tarefas desse usuário também fossem excluídas
            # ou reatribuídas (TaskRepository.delete_tasks_by_user_id(user_id)).
            return True
        else:
            print(f"Falha ao deletar usuário ID {user_id}.")
            return False
