import sqlite3
import bcrypt

DB_PATH = "users.db"


def get_connection():
    """
    Open a connection to users database. 
    """
    db_connection = sqlite3.connect(DB_PATH)
    db_connection.row_factory = sqlite3.Row
    return db_connection

def init_db():
    """
    create users table 
    """
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id        INTEGER PRIMARY KEY AUTOINCREMENT, 
                app_id         TEXT NOT NULL,
                username       TEXT NOT NULL,
                password_hash  TEXT NOT NULL,
                UNIQUE (app_id, username) 
            )
        """)
        conn.commit()
    finally:
        conn.close()

def register_user(app_id, username, password):
    """
    Saves a user with hashed password. 
    Returns new user without password, or None if taken
    """
    password_hash = hash_password(password)

    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (app_id, username, password_hash) VALUES (?, ?, ?)",
            (app_id, username, password_hash) 
        )
        conn.commit()
        return {"user_id": cursor.lastrowid, "app_id": app_id, "username": username}
    
    except sqlite3.IntegrityError:
        return None
    
    finally:
        conn.close()


def get_user(app_id, username):
    """
    return user record including password hash
    """
    conn = get_connection()
    
    try:
        cursor = conn.execute(
            "SELECT * FROM users WHERE app_id=? AND username=?",
                (app_id, username) 
            )
        row = cursor.fetchone()

        if row is None:
            return None
        
        return dict(row)
      
    finally:
        conn.close()


def hash_password(password):
    """
    hash text password
    """
    password_bytes = password.encode("utf-8") #convert text password to bytes first
    salt = bcrypt.gensalt() #make a random salt so identical passwords can get diff hashes

    hash_bytes = bcrypt.hashpw(password_bytes, salt) #mix salt and pw now
    hash_text = hash_bytes.decode("utf-8") # convert bytes back to text

    return hash_text


def check_password(password, password_hash):
    """
    Return true if password matches the stored hash
    """

    pw_bytes = password.encode("utf-8") #convert text password to bytes 
    if len(pw_bytes) > 72:
        return False

    stored_bytes = password_hash.encode("utf-8") #convert stored hash password to bytes 

    matches = bcrypt.checkpw(pw_bytes, stored_bytes) #hashes pw and compares to stored hash
    return matches
