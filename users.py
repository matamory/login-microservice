def init_db():
    """
    *** Yesenia Task ***
    TODO: create users table 
    """
    pass

def register_user(app_id, username, password):
    """
    *** Yesenia Task ***
    TODO: hash password, save user
    Returns new user without password, or None if taken
    """
    return {"user_id": 1,"app_id": app_id, "username": username}

def get_user(app_id, username):
    """
    *** Yesenia Task ***
    TODO: return user record including password hash
    """
    return None

def check_password(password, password_hash):
    """
    *** Yesenia Task ***
    TODO: return true if password matches the stored hash
    """
    return False
