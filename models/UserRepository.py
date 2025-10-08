import sqlite3
from typing import List, Tuple, Optional

class UserRepository:
    """
    Model/Repository responsável pelas operações CRUD na tabela 'usuarios'.
    """
    
    def __init__(self, db_name: str = 'taskDB.db'):
        """
        Inicializa o Repository e garante que a tabela de usuários exista.
        O db_name é mantido igual ao TaskRepository para usar o mesmo arquivo.
        """
        self.db_name = db_name
        self.create_tables()

    def _execute(self, query: str, params: Tuple = (), commit: bool = False) -> Optional[List[Tuple]]:
        # Método auxiliar para execução de SQL (reutilizado do TarefaRepository)
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
            print(f"Erro no banco de dados (User): {e}")
            return None
        finally:
            if conn:
                conn.close()

    def create_tables(self):
        """
        Cria a tabela 'usuarios' com os campos necessários (nome, email, admin).
        A senha_hash é apenas um placeholder simples aqui.
        """
        self._execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL UNIQUE,
            email TEXT,
            senha_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        );
        """, commit=True)
        
    # --- Operações CRUD (Mapeadas para o UserManager) ---

    def adicionar_usuario(self, nome_usuario: str, email: str, is_admin: bool) -> Optional[int]:
        """
        Insere um novo usuário. Retorna o ID do usuário inserido ou None em caso de erro.
        Usa uma senha hash simples (A senha real deve ser tratada com bcrypt ou similar).
        """
        senha_default_hash = "placeholder_hash" 
        is_admin_int = 1 if is_admin else 0
        
        query = """
        INSERT INTO usuarios (nome_usuario, email, senha_hash, is_admin)
        VALUES (?, ?, ?, ?);
        """
        # Execute com uma nova lógica para obter o último ID inserido
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(query, (nome_usuario, email, senha_default_hash, is_admin_int))
            conn.commit()
            return cursor.lastrowid # Retorna o ID da última linha inserida
        except sqlite3.IntegrityError:
            print(f"Usuário '{nome_usuario}' já existe.")
            return None
        except sqlite3.Error as e:
            print(f"Erro ao inserir usuário: {e}")
            return None
        finally:
            conn.close()


    def buscar_usuario_por_id(self, user_id: int) -> Optional[Tuple]:
        """
        Busca um usuário pelo ID.
        Retorna uma tupla: (id, nome_usuario, email, senha_hash, is_admin)
        """
        query = "SELECT id, nome_usuario, email, is_admin FROM usuarios WHERE id = ?;"
        result = self._execute(query, (user_id,))
        return result[0] if result else None
    
    def buscar_usuario_por_username(self, username: str) -> Optional[Tuple]:
        """
        Busca um usuário pelo nome de usuário.
        """
        query = "SELECT id, nome_usuario, email, is_admin FROM usuarios WHERE nome_usuario = ?;"
        result = self._execute(query, (username,))
        return result[0] if result else None

    def buscar_todos_usuarios(self) -> List[Tuple]:
        """
        Retorna todos os usuários no formato de tuplas.
        """
        query = "SELECT id, nome_usuario, email, is_admin FROM usuarios;"
        return self._execute(query) or []
