# TaskManager.py (Seu Controller)

from typing import List
# Importa o Model (Repository)
from models.TarefaRepository import TarefaRepository 
# Importa a classe Tarefa (para encapsulamento de dados, se necessário)
# from models.Tarefa import Tarefa # Manter se a classe Tarefa for usada para retorno

class TaskManager:
    """
    Controlador (C do MVC) para gerenciar a lógica de negócios das tarefas.
    Ele utiliza o TarefaRepository para persistir os dados.
    """
    
    def __init__(self, db_name='taskDB.db'):
        # 1. O Controller instancia o Model/Repository
        self.model = TarefaRepository(db_name) 

    # --- CRUD: CREATE ---
    def addTask(self, description: str, userId: int) -> bool:
        """ Adiciona uma nova tarefa ao banco de dados. """
        if not description.strip():
            return False
            
        # O Controller chama o método do Model, passando apenas os dados
        return self.model.adicionar_tarefa(userId, description.strip()) 
        # Nota: O Controller decide retornar True/False se a inserção for bem-sucedida

    # --- CRUD: READ ---
    def getTasksForUser(self, userId: int) -> List[dict]:
        """ 
        Busca tarefas do usuário no BD e as formata para a View.
        Retorna uma lista de dicionários para facilitar o uso na interface.
        """
        # 1. Chama o Model para obter os dados brutos (Tuplas: id, descricao, concluida)
        tarefas_raw = self.model.buscar_tarefas_por_usuario(userId)
        
        # 2. Formata os dados no Controller (opcional, mas recomendado)
        tarefas_formatadas = []
        for id_tarefa, descricao, concluida in tarefas_raw:
            tarefas_formatadas.append({
                'id': id_tarefa,
                'descricao': descricao,
                'concluida': concluida == 1  # Converte 0/1 para True/False
            })
            
        return tarefas_formatadas

    # --- CRUD: UPDATE ---
    def markTaskCompleted(self, taskId: int, userId: int, completed: bool = True) -> bool:
        """
        Marca uma tarefa como concluída (True) ou pendente (False).
        
        NOTA CRÍTICA: Como o Model exige a 'descrição' na função 'atualizar_tarefa', 
        precisamos primeiro buscar a descrição atual da tarefa.
        """
        # 1. Busca todas as tarefas do usuário
        tarefas_atuais = self.getTasksForUser(userId)
        
        # 2. Encontra a tarefa específica pelo ID
        tarefa_encontrada = next((t for t in tarefas_atuais if t['id'] == taskId), None)
        
        if tarefa_encontrada:
            descricao_atual = tarefa_encontrada['descricao']
            status_int = 1 if completed else 0
            
            # 3. Chama o Model para atualizar o status (e passa a descrição atual)
            return self.model.atualizar_tarefa(
                tarefa_id=taskId, 
                id_usuario=userId, 
                nova_descricao=descricao_atual, 
                concluida=status_int
            )
            
        return False
        
    def updateTaskDescription(self, taskId: int, userId: int, new_description: str) -> bool:
        """ 
        Atualiza apenas a descrição da tarefa, mantendo o status 'concluida'.
        """
        # 1. Busca todas as tarefas do usuário
        tarefas_atuais = self.getTasksForUser(userId)
        
        # 2. Encontra a tarefa específica para obter o status 'concluida'
        tarefa_encontrada = next((t for t in tarefas_atuais if t['id'] == taskId), None)

        if tarefa_encontrada:
            status_int = 1 if tarefa_encontrada['concluida'] else 0
            
            # 3. Chama o Model para atualizar a descrição (e passa o status atual)
            return self.model.atualizar_tarefa(
                tarefa_id=taskId, 
                id_usuario=userId, 
                nova_descricao=new_description.strip(), 
                concluida=status_int
            )
        
        return False


    # --- CRUD: DELETE ---
    def deleteTask(self, taskId: int, userId: int) -> bool:
        """ Remove a tarefa do banco de dados, verificando o ID do usuário. """
        return self.model.excluir_tarefa(taskId, userId)
    
    
    # --- Funções Específicas do Projeto ---
    
    # Este método DEVE ser movido para um "UserController" ou "AdminController" 
    # por envolver a lógica de múltiplos usuários.
    def addTaskEveryone(self, description: str, user_manager) -> None:
        """ Adiciona uma tarefa para todos os usuários. """
        if not description.strip():
            return
            
        for user in user_manager.getAllUsers():
            # Chama a função principal de adicionar tarefa para cada usuário
            self.addTask(description, user.getId())
