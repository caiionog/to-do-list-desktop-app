from models.Pessoa import Pessoa

class UserManager:
    def __init__(self):
        self._all_users = []
        self._next_user_id = 1 

    def addUser(self, username, email, isAdmin):
        new_user = Pessoa(self._next_user_id, username, email, isAdmin)
        self._all_users.append(new_user)
        self._next_user_id += 1 
        return new_user
    
    def getUserById(self, userId):
        for user in self._all_users:
            if user.getId() == userId:
                return user
        return None 
        
    def getAllUsers(self):
        return self._all_users