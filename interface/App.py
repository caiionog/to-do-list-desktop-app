import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sys

# --- CLASSE PRINCIPAL DA APLICAÇÃO ---
class App(ctk.CTk):
    def __init__(self, auth_controller, user_manager=None, task_manager=None):
        super().__init__()

        # --- Configurações CustomTkinter ---
        # Define o tema padrão da aplicação: 'Light', 'Dark', ou 'System'
        ctk.set_appearance_mode("System") 
        # Define o tema de cor (azul, verde, ou dark-blue)
        ctk.set_default_color_theme("blue") 
        # -----------------------------------

        self.title("Sistema de Gerenciamento de Tarefas")
        self.geometry("450x350")
        self.resizable(False, False)
        
        # Mantenha as referências aos controladores
        self.auth_controller = auth_controller
        self.user_manager = user_manager
        self.task_manager = task_manager
        
        self.current_user = None
        
        # Container para os Frames (Telas)
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid(row=0, column=0, sticky="nsew") # Usamos grid e sticky para o container
        
        self.frames = {}
        
        # CRIAÇÃO DE TODOS OS FRAMES
        for F in (LoginFrame, UserMenuFrame, AdminMenuFrame, CreateTaskFrame, ManageTasksFrame, CreateUserFrame, CreateTaskForUserFrame, CreateTaskForEveryoneFrame, DeleteUserFrame, SelectUserTasksFrame, AdminManageTasksFrame): 
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        '''Mostra um frame para o nome de página dado'''
        frame = self.frames[page_name]
        
        # O frame de gerenciamento de usuário normal também precisa ser atualizado
        if page_name == "ManageTasksFrame":
            frame.update_task_list() 
        
        # O frame de gerenciamento de Admin também precisa ser atualizado
        if page_name == "AdminManageTasksFrame":
            frame.update_task_list()
            
        frame.tkraise()

    def set_current_user(self, user):
        self.current_user = user
        if user:
            print(f"Usuário Logado: {user.getUsername()}")
            self.frames["UserMenuFrame"].update_menu() 
            self.show_frame("UserMenuFrame") 
        else:
            print("Usuário deslogado.")
            self.show_frame("LoginFrame")

# --- CLASSE DA TELA DE LOGIN (Sem alteração relevante) ---
class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Login ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        ctk.CTkLabel(self, text="Digite seu ID:").pack(pady=(10, 0))
        self.id_entry = ctk.CTkEntry(self, width=300)
        self.id_entry.pack(pady=5, fill="x", padx=40)
        
        ctk.CTkButton(self, text="Fazer Login", command=self.perform_login).pack(pady=10)
        
        ctk.CTkButton(self, text="Sair do Aplicativo", command=sys.exit).pack(pady=10)

    def perform_login(self):
        try:
            user_id = int(self.id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erro de Login", "O ID deve ser um número inteiro.")
            return

        user = self.controller.auth_controller.login(user_id)
        
        if user:
            messagebox.showinfo("Login Bem-Sucedido", f"Bem-vindo, {user.getUsername()}!")
            self.id_entry.delete(0, tk.END) # Limpa o campo
            self.controller.set_current_user(user)
        else:
            messagebox.showerror("Erro de Login", "ID inválido. Tente novamente.")
            self.id_entry.delete(0, tk.END)

# --- CLASSE DA TELA DE MENU DE ADMINISTRADOR (COM BOTÃO DE VOLTA) ---
class AdminMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Menu de Administrador ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Opções do menu Admin
        ctk.CTkButton(self, text="Criar Novo Usuário", 
                  command=lambda: controller.show_frame("CreateUserFrame")).pack(pady=5, ipadx=10)
        
        ctk.CTkButton(self, text="Criar Tarefa para Usuário", 
                  command=lambda: controller.show_frame("CreateTaskForUserFrame")).pack(pady=5, ipadx=10)
        
        ctk.CTkButton(self, text="Criar Tarefa para Todos", 
                  command=lambda: controller.show_frame("CreateTaskForEveryoneFrame")).pack(pady=5, ipadx=10)
        
        ctk.CTkButton(self, text="Excluir Usuário", 
                  command=lambda: controller.show_frame("DeleteUserFrame")).pack(pady=5, ipadx=10)
        
        ctk.CTkButton(self, text="Gerenciar Tarefas de Usuário", 
                  command=lambda: controller.show_frame("SelectUserTasksFrame")).pack(pady=5, ipadx=10)

        # 0. Voltar ao Menu Principal (para o UserMenuFrame)
        ctk.CTkButton(self, text="Voltar ao Menu Principal", 
                  command=lambda: controller.show_frame("UserMenuFrame")).pack(pady=20, ipadx=10)
        
    def admin_action(self, action):
        user = self.controller.current_user
        if user:
            messagebox.showinfo("Ação de Admin", f"Admin {user.getUsername()} executou a ação: {action}")
            
    def update_menu(self):
        # Lógica para atualizar a visualização ao entrar na tela
        pass

# --- CLASSE DA TELA DE MENU DE USUÁRIO (Acesso aos sub-menus) ---
class UserMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Menu ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # NOVO: Vai para a tela de Criação de Tarefas
        ctk.CTkButton(self, text="Criar Nova Tarefa", 
                  command=lambda: self.controller.show_frame("CreateTaskFrame")).pack(pady=5, ipadx=10)
        
        # NOVO: Vai para a tela de Gerenciamento de Tarefas
        ctk.CTkButton(self, text="Gerenciar Minhas Tarefas", 
                  command=lambda: self.controller.show_frame("ManageTasksFrame")).pack(pady=5, ipadx=10)
        
        ctk.CTkButton(self, text="Logout", 
                  command=lambda: controller.set_current_user(None)).pack(pady=20, ipadx=10)

        # Botão Admin (Condicional)
        self.admin_btn = ctk.CTkButton(self, text="Menu Admin", 
                                   command=lambda: self.controller.show_frame("AdminMenuFrame"))
        
    def update_menu(self):
        # Lógica crucial: Mostrar o botão "Menu Admin" apenas se for admin
        user = self.controller.current_user
        if user and user.isAdmin():
            self.admin_btn.pack(pady=5, ipadx=10)
        else:
            self.admin_btn.pack_forget()

# --- NOVO SUB-MENU: CRIAÇÃO DE TAREFAS ---
class CreateTaskFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Criar Nova Tarefa ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Input: Descrição da Tarefa
        ctk.CTkLabel(self, text="Descrição da Tarefa:").pack(pady=(10, 0))
        self.description_entry = ctk.CTkEntry(self, width=400)
        self.description_entry.pack(pady=5, fill="x", padx=40)
        
        # Botão: Salvar Tarefa
        ctk.CTkButton(self, text="Salvar Tarefa", command=self.create_task).pack(pady=10)
        
        # Botão: Voltar
        ctk.CTkButton(self, text="Voltar ao Menu", 
                  command=lambda: controller.show_frame("UserMenuFrame")).pack(pady=20)

    def create_task(self):
    # 1. CAPTURA DOS DADOS
        description = self.description_entry.get().strip() # Captura e remove espaços
        user = self.controller.current_user
    
        if not description:
            messagebox.showwarning("Atenção", "A descrição da tarefa não pode estar vazia.")
            return

        # 2. VALIDAÇÃO E CHAMADA AO BACKEND
        if user and self.controller.task_manager:
            try:
                user_id = user.getId() # Garante que estamos pegando o ID corretamente
            
            # CHAMA SEU MÉTODO addTask COM OS PARÂMETROS
            # Verifique se o seu addTask retorna algo que indique sucesso ou falha (True/False)
                success = self.controller.task_manager.addTask(description, user_id)
            
                if success: # Assumindo que seu addTask retorna True em caso de sucesso
                    messagebox.showinfo("Sucesso", "Tarefa criada com sucesso!")
                    self.description_entry.delete(0, tk.END) # Limpa o campo
                    self.controller.show_frame("UserMenuFrame") # Volta ao menu
                else:
                    messagebox.showerror("Erro", "A tarefa não foi salva pelo sistema (erro interno do backend).")
                 
            except Exception as e:
            # Captura qualquer erro de execução do seu método addTask
                messagebox.showerror("Erro", f"Falha catastrófica ao criar tarefa: {e}")
        else:
            messagebox.showerror("Erro", "Usuário não logado ou gerenciador de tarefas indisponível.")

# --- NOVO SUB-MENU: GERENCIAMENTO DE TAREFAS (Exemplo simplificado) ---
class ManageTasksFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Gerenciar Minhas Tarefas ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Listbox para exibir as tarefas
        self.task_listbox = tk.Listbox(self, width=50, height=10) # <--- CORRIGIDO!
        self.task_listbox.pack(pady=10)

        # Botões de Ação
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)
        
        ctk.CTkButton(btn_frame, text="Marcar Concluída", 
                  command=self.mark_completed).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar Tarefa", 
                  command=self.delete_task).pack(side=tk.LEFT, padx=5)
        
        # Botão Voltar
        ctk.CTkButton(self, text="Voltar ao Menu", 
                  command=lambda: controller.show_frame("UserMenuFrame")).pack(pady=20)

    def update_task_list(self):
        '''Popula a Listbox obtendo as tarefas através da função viewTask do usuário logado.'''
        self.task_listbox.delete(0, tk.END)
        user = self.controller.current_user
        
        tasks = [] # Inicialização segura

        if user and self.controller.task_manager:
            try:
                # tasks_result recebe uma lista de dicionários do user.viewTask()
                tasks_result = user.viewTask(self.controller.task_manager)
                
                # Garante que o resultado é uma lista, não None
                if tasks_result is not None:
                    tasks = tasks_result
                
            except AttributeError:
                messagebox.showerror("Erro de View", "O objeto de Usuário não possui o método 'viewTask'.")
                return
            except Exception as e:
                messagebox.showerror("Erro de Backend", f"Falha ao carregar tarefas: {e}")
                return
                
        # Itera sobre a lista de DICIONÁRIOS
        for task in tasks:
            # ⚠️ CORREÇÃO APLICADA: Acessando chaves de dicionário [key]
            
            task_id = task.get('id', 'N/A')
            descricao = task.get('descricao', 'Sem Descrição')
            concluida = task.get('concluida', False) # A chave é 'concluida'
            
            status = "Concluída" if concluida else "Pendente"
            
            # Insere na Listbox usando os valores do dicionário
            self.task_listbox.insert(tk.END, f"[{task_id}] {descricao} ({status})")


    def get_selected_task_id(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Atenção", "Selecione uma tarefa na lista.")
            return None
            
        # Pega o texto da linha selecionada (ex: "[1] Tarefa...")
        selected_text = self.task_listbox.get(selected_index[0])
        try:
            # Extrai o ID entre os colchetes
            task_id = int(selected_text.split(']')[0].strip('['))
            return task_id
        except:
            return None


    def mark_completed(self):
        task_id = self.get_selected_task_id()
        user = self.controller.current_user
        
        if task_id and user:
            # Chama o método real de backend
            if self.controller.task_manager.markTaskCompleted(task_id, user.getId()):
                messagebox.showinfo("Sucesso", f"Tarefa ID {task_id} marcada como concluída.")
                self.update_task_list() # Atualiza a Listbox
            else:
                 messagebox.showerror("Erro", "Falha ao concluir tarefa ou ID inválido.")
                 

    def delete_task(self):
        task_id = self.get_selected_task_id()
        user = self.controller.current_user
        
        if task_id and user and messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar a Tarefa ID: {task_id}?"):
            # Chama o método real de backend
            if self.controller.task_manager.deleteTask(task_id, user.getId()):
                messagebox.showinfo("Sucesso", f"Tarefa ID {task_id} deletada com sucesso.")
                self.update_task_list() # Atualiza a Listbox
            else:
                messagebox.showerror("Erro", "Falha ao deletar tarefa ou ID inválido.")

class CreateUserFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Criar Novo Usuário ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Campo Nome de Usuário
        ctk.CTkLabel(self, text="Nome de Usuário:").pack(pady=(10, 0))
        self.username_entry = ctk.CTkEntry(self, width=400)
        self.username_entry.pack(pady=5, fill="x", padx=40)

        # Campo Email
        ctk.CTkLabel(self, text="Email:").pack(pady=(10, 0))
        self.email_entry = ctk.CTkEntry(self, width=400)
        self.email_entry.pack(pady=5, fill="x", padx=40)
        
        # Campo Status Admin (usaremos um Checkbutton)
        self.is_admin_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self, text="Conceder Permissões de Admin", variable=self.is_admin_var).pack(pady=10)
        
        # Botão: Salvar Usuário
        ctk.CTkButton(self, text="Criar Usuário", command=self.create_user).pack(pady=10)
        
        # Botão: Voltar
        ctk.CTkButton(self, text="Voltar ao Menu Admin", 
                  command=lambda: controller.show_frame("AdminMenuFrame")).pack(pady=20)

    def create_user(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        is_admin = self.is_admin_var.get()
        
        if not username or not email:
            messagebox.showwarning("Atenção", "Nome de usuário e Email são obrigatórios.")
            return

        if self.controller.user_manager:
            try:
                # Chama a lógica do seu backend
                # Assumindo que seu user_manager.addUser(username, email, is_admin) funciona.
                new_user = self.controller.user_manager.addUser(username, email, is_admin)
                
                if new_user: # Assumindo que addUser retorna o novo objeto User ou True
                    messagebox.showinfo("Sucesso", f"Usuário '{username}' criado com sucesso! ID: {new_user.getId()}")
                    
                    # Limpa os campos e volta ao menu
                    self.username_entry.delete(0, tk.END)
                    self.email_entry.delete(0, tk.END)
                    self.is_admin_var.set(False)
                    self.controller.show_frame("AdminMenuFrame")
                else:
                    messagebox.showerror("Erro", "Falha ao criar usuário. (Verifique o backend)")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha catastrófica ao criar usuário: {e}")
        else:
            messagebox.showerror("Erro", "Gerenciador de Usuários (user_manager) indisponível.")

class CreateTaskForUserFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Criar Tarefa para Usuário ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Campo ID do Usuário Alvo
        ctk.CTkLabel(self, text="ID do Usuário Alvo:").pack(pady=(10, 0))
        self.user_id_entry = ctk.CTkEntry(self, width=400)
        self.user_id_entry.pack(pady=5, fill="x", padx=40)
        
        # Campo Descrição da Tarefa
        ctk.CTkLabel(self, text="Descrição da Tarefa:").pack(pady=(10, 0))
        self.description_entry = ctk.CTkEntry(self, width=400)
        self.description_entry.pack(pady=5, fill="x", padx=40)
        
        # Botão: Salvar Tarefa
        ctk.CTkButton(self, text="Atribuir Tarefa", command=self.create_task_for_user).pack(pady=10)
        
        # Botão: Voltar
        ctk.CTkButton(self, text="Voltar ao Menu Admin", 
                  command=lambda: controller.show_frame("AdminMenuFrame")).pack(pady=20)

    def create_task_for_user(self):
        description = self.description_entry.get().strip()
        user_id_str = self.user_id_entry.get().strip()
        
        if not description or not user_id_str:
            messagebox.showwarning("Atenção", "O ID do Usuário e a Descrição da Tarefa são obrigatórios.")
            return

        try:
            user_id = int(user_id_str)
        except ValueError:
            messagebox.showerror("Erro de Input", "O ID do Usuário deve ser um número inteiro.")
            return

        if self.controller.user_manager and self.controller.task_manager:
            try:
                # 1. Verifica se o usuário alvo existe
                user_alvo = self.controller.user_manager.getUserById(user_id)
                
                if user_alvo is None:
                    messagebox.showerror("Erro", f"Usuário com ID {user_id} não encontrado.")
                    return
                
                # 2. Chama a lógica do seu backend
                success = self.controller.task_manager.addTask(description, user_id)
                
                if success: # Assumindo que addTask retorna True em caso de sucesso
                    messagebox.showinfo("Sucesso", f"Tarefa criada e atribuída a '{user_alvo.getUsername()}' (ID: {user_id}).")
                    
                    # Limpa os campos e volta ao menu
                    self.user_id_entry.delete(0, tk.END)
                    self.description_entry.delete(0, tk.END)
                    self.controller.show_frame("AdminMenuFrame")
                else:
                    messagebox.showerror("Erro", "Falha ao salvar a tarefa no sistema (erro interno do backend).")
            
            except Exception as e:
                messagebox.showerror("Erro", f"Falha catastrófica ao criar tarefa: {e}")
        else:
            messagebox.showerror("Erro", "Gerenciadores (User/Task) indisponíveis.")

class CreateTaskForEveryoneFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Atribuir Tarefa Global ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Campo Descrição da Tarefa
        ctk.CTkLabel(self, text="Descrição da Tarefa para TODOS:").pack(pady=(10, 0))
        self.description_entry = ctk.CTkEntry(self, width=400)
        self.description_entry.pack(pady=5, fill="x", padx=40)
        
        # Botão: Salvar Tarefa
        ctk.CTkButton(self, text="Atribuir a Todos", command=self.create_task_for_everyone).pack(pady=10)
        
        # Botão: Voltar
        ctk.CTkButton(self, text="Voltar ao Menu Admin", 
                  command=lambda: controller.show_frame("AdminMenuFrame")).pack(pady=20)

    def create_task_for_everyone(self):
        description = self.description_entry.get().strip()
        
        if not description:
            messagebox.showwarning("Atenção", "A Descrição da Tarefa é obrigatória.")
            return

        if self.controller.user_manager and self.controller.task_manager:
            try:
                # ⚠️ CHAMADA AO BACKEND:
                # Chama a lógica que atribui a tarefa a todos os usuários
                # Assumindo que seu addTaskEveryone retorna True/False ou algo que indique sucesso.
                
                success = self.controller.task_manager.addTaskEveryone(description, self.controller.user_manager)
                
                if success:
                    messagebox.showinfo("Sucesso", "Tarefa criada e atribuída a TODOS os usuários ativos.")
                    
                    # Limpa o campo e volta ao menu
                    self.description_entry.delete(0, tk.END)
                    self.controller.show_frame("AdminMenuFrame")
                else:
                    messagebox.showerror("Erro", "Falha ao salvar a tarefa global (erro interno do backend).")
            
            except Exception as e:
                messagebox.showerror("Erro", f"Falha catastrófica ao criar tarefa global: {e}")
        else:
            messagebox.showerror("Erro", "Gerenciadores (User/Task) indisponíveis.")

# --- NOVO SUB-MENU: EXCLUIR USUÁRIO (Apenas para Admin) ---
class DeleteUserFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Excluir Usuário ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Campo ID do Usuário a ser Excluído
        ctk.CTkLabel(self, text="ID do Usuário a ser Excluído:").pack(pady=(10, 0))
        self.user_id_entry = ctk.CTkEntry(self, width=400)
        self.user_id_entry.pack(pady=5, fill="x", padx=40)
        
        # Botão: Excluir Usuário
        ctk.CTkButton(self, text="Excluir Usuário", command=self.delete_user).pack(pady=10)
        
        # Botão: Voltar
        ctk.CTkButton(self, text="Voltar ao Menu Admin", 
                  command=lambda: controller.show_frame("AdminMenuFrame")).pack(pady=20)

    def delete_user(self):
        user_id_str = self.user_id_entry.get().strip()
        current_admin = self.controller.current_user
        
        if not user_id_str:
            messagebox.showwarning("Atenção", "O ID do Usuário é obrigatório.")
            return

        try:
            user_id_to_delete = int(user_id_str)
        except ValueError:
            messagebox.showerror("Erro de Input", "O ID deve ser um número inteiro.")
            return

        # 1. VALIDAÇÃO DE SEGURANÇA: Não permitir exclusão do próprio Admin
        if current_admin and user_id_to_delete == current_admin.getId():
            messagebox.showerror("Erro de Segurança", "Você não pode excluir a si mesmo.")
            self.user_id_entry.delete(0, tk.END)
            return

        if self.controller.user_manager:
            # 2. Confirmação Gráfica da Ação
            confirm = messagebox.askyesno(
                "Confirmação de Exclusão", 
                f"Tem certeza que deseja excluir o usuário com ID: {user_id_to_delete}?"
            )
            
            if confirm:
                try:
                    # Tenta obter o usuário para ver se existe
                    user_to_delete = self.controller.user_manager.getUserById(user_id_to_delete)
                    
                    if user_to_delete is None:
                        messagebox.showerror("Erro", f"Usuário com ID {user_id_to_delete} não encontrado.")
                        return

                    # 3. CHAMA A LÓGICA DO BACKEND: Excluir Usuário
                    # Assumindo que user_manager.deleteUser(id) ou similar retorna True em sucesso.
                    success = self.controller.user_manager.deleteUser(user_to_delete) 

                    if success:
                        messagebox.showinfo("Sucesso", f"Usuário '{user_to_delete.getUsername()}' excluído com sucesso.")
                        self.user_id_entry.delete(0, tk.END)
                        self.controller.show_frame("AdminMenuFrame")
                    else:
                        messagebox.showerror("Erro", "Falha ao excluir o usuário (erro interno do backend).")

                except Exception as e:
                    messagebox.showerror("Erro", f"Falha catastrófica ao excluir usuário: {e}")
            
        else:
            messagebox.showerror("Erro", "Gerenciador de Usuários (user_manager) indisponível.")

# --- NOVO SUB-MENU 1: SELECIONAR USUÁRIO PARA GERENCIAMENTO ---
class SelectUserTasksFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="--- Gerenciar Tarefas de Usuário ---", font=('Arial', 18, 'bold')).pack(pady=10)
        
        ctk.CTkLabel(self, text="Digite o ID do Usuário Alvo:").pack(pady=(10, 0))
        self.user_id_entry = ctk.CTkEntry(self, width=400)
        self.user_id_entry.pack(pady=5, fill="x", padx=40)
        
        # Botão: Abrir Gerenciamento
        ctk.CTkButton(self, text="Abrir Tarefas do Usuário", command=self.open_task_management).pack(pady=10)
        
        # Botão: Voltar
        ctk.CTkButton(self, text="Voltar ao Menu Admin", 
                  command=lambda: controller.show_frame("AdminMenuFrame")).pack(pady=20)

    def open_task_management(self):
        user_id_str = self.user_id_entry.get().strip()
        
        if not user_id_str:
            messagebox.showwarning("Atenção", "O ID do Usuário é obrigatório.")
            return

        try:
            user_id = int(user_id_str)
        except ValueError:
            messagebox.showerror("Erro de Input", "O ID do Usuário deve ser um número inteiro.")
            return

        if self.controller.user_manager:
            try:
                user_alvo = self.controller.user_manager.getUserById(user_id)
                
                if user_alvo is None:
                    messagebox.showerror("Erro", f"Usuário com ID {user_id} não encontrado.")
                    return
                
                # ⚠️ PASSAGEM DO CONTEXTO: Guarda o objeto do usuário alvo no controlador
                self.controller.user_alvo_admin_view = user_alvo
                
                # Vai para o Frame de gerenciamento, que usará o contexto salvo
                self.controller.show_frame("AdminManageTasksFrame")
                
                # Limpa o campo após o sucesso
                self.user_id_entry.delete(0, tk.END)

            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao buscar usuário: {e}")
        else:
            messagebox.showerror("Erro", "Gerenciador de Usuários indisponível.")


# --- NOVO SUB-MENU 2: GERENCIAR TAREFAS DE ADMIN (Abre a Listbox) ---
class AdminManageTasksFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.title_label = ctk.CTkLabel(self, text="Gerenciar Tarefas", font=('Arial', 18, 'bold'))
        self.title_label.pack(pady=10)

        # Listbox para exibir as tarefas
        self.task_listbox = tk.Listbox(self, width=60, height=10) # <--- CORRIGIDO!
        self.task_listbox.pack(pady=10)

        # Botões de Ação
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)
        
        ctk.CTkButton(btn_frame, text="Marcar Concluída", 
                  command=self.mark_completed).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar Tarefa", 
                  command=self.delete_task).pack(side=tk.LEFT, padx=5)
        
        # Botão Voltar (Volta para a tela de seleção de ID)
        ctk.CTkButton(self, text="Voltar à Seleção de Usuário", 
                  command=lambda: controller.show_frame("SelectUserTasksFrame")).pack(pady=20)

    def update_task_list(self):
        '''Popula a Listbox com as tarefas do usuário alvo selecionado pelo Admin.'''
        self.task_listbox.delete(0, tk.END)
        
        # 1. Tenta obter o usuário alvo da variável de contexto do controlador
        # Usamos getattr para não quebrar se a variável ainda não existir (retorna None)
        user_alvo = getattr(self.controller, 'user_alvo_admin_view', None)
        
        tasks = [] # Inicialização segura
        
        if user_alvo and self.controller.task_manager:
            # Atualiza o título
            self.title_label.configure(text=f"Gerenciar Tarefas de: {user_alvo.getUsername()}")
            
            try:
                # 2. CHAMADA AO BACKEND: Obtém tarefas do usuário alvo (Retorna lista de dicionários)
                tasks_result = user_alvo.viewTask(self.controller.task_manager)
                
                if tasks_result is not None:
                    tasks = tasks_result
                    
            except AttributeError:
                # Exibe erro se o objeto User não tiver o método viewTask
                messagebox.showerror("Erro de View", "O objeto de Usuário Alvo não possui o método 'viewTask'.")
                return
            except Exception as e:
                messagebox.showerror("Erro de Backend", f"Falha ao carregar tarefas: {e}")
                return
                
            # 3. Itera sobre a lista de DICIONÁRIOS e insere na Listbox
            for task in tasks:
                # Acessando chaves de dicionário (.get)
                task_id = task.get('id', 'N/A')
                descricao = task.get('descricao', 'Sem Descrição')
                concluida = task.get('concluida', False)
                
                status = "Concluída" if concluida else "Pendente"
                self.task_listbox.insert(tk.END, f"[{task_id}] {descricao} ({status})")
        else:
            # Caso o Frame seja aberto sem que o usuário alvo tenha sido selecionado
            self.title_label.configure(text="Erro: Usuário Alvo Não Selecionado")


    def get_selected_task_id(self):
        # (Função idêntica à do ManageTasksFrame normal para extrair ID)
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Atenção", "Selecione uma tarefa na lista.")
            return None
            
        selected_text = self.task_listbox.get(selected_index[0])
        try:
            task_id = int(selected_text.split(']')[0].strip('['))
            return task_id
        except:
            return None

    def mark_completed(self):
        task_id = self.get_selected_task_id()
        user_alvo = getattr(self.controller, 'user_alvo_admin_view', None)
        
        if task_id and user_alvo:
            # Chama o método de backend usando o ID do USUÁRIO ALVO
            if self.controller.task_manager.markTaskCompleted(task_id, user_alvo.getId()):
                messagebox.showinfo("Sucesso", f"Tarefa ID {task_id} de {user_alvo.getUsername()} marcada como concluída.")
                self.update_task_list()
            else:
                 messagebox.showerror("Erro", "Falha ao concluir tarefa ou ID inválido.")
                 
    def delete_task(self):
        task_id = self.get_selected_task_id()
        user_alvo = getattr(self.controller, 'user_alvo_admin_view', None)
        
        if task_id and user_alvo and messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar a Tarefa ID: {task_id} do usuário {user_alvo.getUsername()}?"):
            # Chama o método de backend usando o ID do USUÁRIO ALVO
            if self.controller.task_manager.deleteTask(task_id, user_alvo.getId()):
                messagebox.showinfo("Sucesso", f"Tarefa ID {task_id} de {user_alvo.getUsername()} deletada com sucesso.")
                self.update_task_list()
            else:
                messagebox.showerror("Erro", "Falha ao deletar tarefa ou ID inválido.")