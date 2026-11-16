from users import get_user, check_password

def login_user(app_id, username, password):
    """
    A function that will return True if credentials passed in are valid, otherwise return False
    """

    user = get_user(app_id, username)

    if user is None:
        return False

    return check_password(password, user["password_hash"])
    