import sqlite3
from typing import List, Tuple, Optional

class TarefaRepository:
    """
    Model (M do MVC) para gerenciar tarefas no SQLite. 
    Foca nas operações CRUD para a tabela 'tarefas', vinculadas a um 'id_usuario'.
    """
    
    def __init__(self, db_name: str = 'tarefas.db'):
        self.db_name = db_name
        self.create_tables()

    def _execute(self, query: str, params: Tuple = (), commit: bool = False) -> Optional[List[Tuple]]:
        # O método auxiliar para execução de SQL permanece o mesmo
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
                return None
            else:
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def create_tables(self):
        """
        Cria a tabela 'usuarios' e a tabela 'tarefas' (sem data_criacao).
        """
        # 1. Tabela de Usuários (necessária para a chave estrangeira)
        self._execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        );
        """, commit=True)
        
        # 2. Tabela de Tarefas (Versão final)
        self._execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0,
            
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id) 
                ON DELETE CASCADE
        );
        """, commit=True)
        
    # --- Operações CRUD ---

    def adicionar_tarefa(self, id_usuario: int, descricao: str) -> bool:
        """
        Insere uma nova tarefa, vinculando-a ao id_usuario.
        """
        query = "INSERT INTO tarefas (id_usuario, descricao, concluida) VALUES (?, ?, 0);"
        result = self._execute(query, (id_usuario, descricao), commit=True)
        return result is None

    def buscar_tarefas_por_usuario(self, id_usuario: int) -> List[Tuple]:
        """
        Retorna SOMENTE as tarefas pertencentes ao id_usuario.
        Ordena pelo ID para ter a ordem de inserção mais recente por último.
        """
        query = """
        SELECT id, descricao, concluida 
        FROM tarefas 
        WHERE id_usuario = ? 
        ORDER BY id DESC;
        """
        # A Tupla retornada agora tem 3 itens: (id, descricao, concluida)
        return self._execute(query, (id_usuario,)) or []

    def atualizar_tarefa(self, tarefa_id: int, id_usuario: int, nova_descricao: str, concluida: int) -> bool:
        """
        Atualiza uma tarefa (descrição e status), garantindo que ela pertença ao id_usuario.
        """
        query = """
        UPDATE tarefas
        SET descricao = ?, concluida = ?
        WHERE id = ? AND id_usuario = ?;
        """
        result = self._execute(query, (nova_descricao, concluida, tarefa_id, id_usuario), commit=True)
        return result is None

    def excluir_tarefa(self, tarefa_id: int, id_usuario: int) -> bool:
        """
        Remove uma tarefa, garantindo que ela pertença ao id_usuario.
        """
        query = "DELETE FROM tarefas WHERE id = ? AND id_usuario = ?;"
        result = self._execute(query, (tarefa_id, id_usuario), commit=True)
        return result is None
