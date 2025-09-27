class AuthController:
    def __init__(self, user_manager):
        self._user_manager = user_manager

    def login(self, id):
        user = self._user_manager.getUserById(id) 
        if user is None:
            return None
        return user 
    