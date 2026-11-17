# Login Microservice

## Description
The Login Microservice allows to register user accounts and verify login credentials.

It uses a REST API and runs on port 5000.

Accounts are separate for each application, so the same username is able to exist across applications without conflicting. Passwords are never stored or returned. Instead, only the salted bycrypt hashes are saved.

The service uses:

- app_id to identify the application
- username to identify the user
- password to verify a user's identity 

The microservice supports:

- POST /register to create a new user account for an application
- POST /login to check that a given username and password exists in current accounts

## Running the microservice

Run app.py first: 

```bash
python3 -m venv venv
source venv/bin/activate   #Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Mac users: note that port 5000 is used by AirPlay Reciever. Toggle off AirDrop & Handoff  in System Settings otherwise requests will return 403.


## How to Request Data

Other programs can request data from the Favorites Microservice by sending HTTP requests to:

http://localhost:5000/register
http://localhost:5000/login


Both endpoints take these fields:

| parameter | type | rules |
| --- | --- | --- |
| app_id  | string | "fitness_tracker", "lens_of_edu", or "medical_journal" |
| username | string | cannot be empty |
| item_id | string | must be at least 12 characters and less than 72 bytes |


## Example call for requesting data
```python
import requests

url = "http://localhost:5000"

login_credentials= {
    "app_id": "fitness_tracker",
    "username": "testuser", 
    "password": "ExPassword123"
}
```


### Register an account
```python
register_response = requests.post(f"{url}/register, json=login_credentials)
```


### Login
```python
login_response = requests.post(f"{url}/login, json=login_credentials)
```


##  How to receive data from the microservice

The Login Microservice returns data in JSON format along with an HTTP status code.

Your program recieves the data by reading the response object: 

response.status_code - gives the status code
response.json() - turns body into Python dictionary 

Body contents:
success - True or False
error - description of error
fields - describe which fields are invalid 



The password is never included in any response. A failed login will return the same message whether the username or password was wrong, in an effort to not reveal which accounts exist. 


| Situation | Status | Response body |
|---|---|---|
| Account registered | 201 | `{"success": true, "user_id": 1, "app_id": "medical_journal", "username": "matamory"}` |
| Login successful | 200 | `{"success": true}` |
| Body is missing or not a JSON object | 400 | `{"success": false, "error": "Invalid or missing JSON"}` |
| One or more fields are missing, blank, or not text (or the password is too short or too long when registering) | 400 | `{"success": false, "error": "Invalid fields", "fields": ["app_id", "username", "password"]}` |
| Wrong password, unknown username, or account belongs to a different app | 401 | `{"success": false, "error": "invalid credentials"}` |
| Username already exists in this app | 409 | `{"success": false, "error": "This username already exists"}` |


## Example call for receiving data

### Check whether the account was created
```python
result = register_response.json()
print(register_response.status_code, result)
```

Output:

```text
201 {'app_id': 'medical_journal', 'success': True, 'user_id': 1, 'username': 'testuser'}
```

### Check whether the login was successful
```
result = login_response.json()

if result["success"]:
    print("Login successful")
else:
    print("Login failed:", result["error"])
```

Output: 
```
Login successful
```

### Handle duplicate username
```
duplicate_response = requests.post(f"{url}/register", json={
    "app_id": "medical_journal",
    "username": "matamory",
    "password": "newpassword1234"
})
print(duplicate_response.status_code, duplicate_response.json()["error"])
```

Output:
```
409 This username already exists
```


### Handle wrong password
```
wrong_response = requests.post(f"{url}/login", json={
    "app_id": "medical_journal",
    "username": "matamory",
    "password": "wrongpass"
})
print(wrong_response.status_code, wrong_response.json()["error"])
```

Output:
```
401 invalid credentials
```

### Handle invalid fields
```
bad_response = requests.post(f"{url}/register", json={"username": "", "password": "pass"})
print(bad_response.status_code, bad_response.json()["fields"])
```

Output:
```
400 ['app_id', 'username', 'password']
```

## UML sequence diagram that communicates how to request and receive data from the microservice


![Register UML sequence diagram] (uml/uml.png)
