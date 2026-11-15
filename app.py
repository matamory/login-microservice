from flask import Flask, request, jsonify

from users import init_db, register_user
from validation import validate_register, validate_login
from auth import login_user


#create web app and initialize db
app = Flask(__name__)
init_db()


#    Error format (all services): {"success": false, "error": "message", "fields": ["password"]} (fields only for validation errors).
#    Status codes: 200 OK · 201 created · 400 invalid input · 401 invalid credentials · 404 not found · 409 duplicate.

# register route
@app.post("/register")
def register():
    data = request.get_json() or {}

    invalid_fields = validate_register(data)
    if invalid_fields:
        return jsonify(success=False, error="Invalid fields", fields=invalid_fields), 400
    
    user = register_user(data["app_id"], data["username"], data["password"])
    if user is None:
        return jsonify(success=False, error="This username already exists"), 409
   
    return jsonify(success=True, **user), 201


# login routes
@app.post("/login")
def login():
    data = request.get_json() or {}

    invalid_fields = validate_login(data)
    if invalid_fields:
        return jsonify(success=False, error="Invalid fields", fields=invalid_fields), 400

    logged_in = login_user(data["app_id"], data["username"], data["password"])
    if logged_in:
        return jsonify(success=True), 200
    
    return jsonify(success=False, error="invalid credentials"), 401


if __name__ == "__main__":
    app.run(port=5000, debug=True)