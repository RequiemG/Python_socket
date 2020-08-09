def login(user_info:dict):
    while True:
        if user_info["username"] == 'zxj' and user_info["password"] == 'qwer':
            return True
        else:
            return False