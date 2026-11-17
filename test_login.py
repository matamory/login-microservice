import requests
import time

BASE_URL = "http://localhost:5000"

#helper functions
def send(endpoint, data):
    url = BASE_URL + endpoint
    response = requests.post(url, json=data)

    print(f"\nREQUEST:\n     POST {endpoint}\n     {data}\n\n")
    print(f"RESPONSE:\n     Status Code: {response.status_code}\n     {response.json()}\n\n")
    return response

#========================== USER STORY 1 ========================== Register a Personal Account
"""

•	Successfully Registering: Given an app_id, an unused username, and a password of at least 12 characters, when the register button is clicked, then the service returns “success” with a new user_id, app_id, and username, without returning the password.
•	Duplicate user attempt: Given a username that is already registered within the same app_id, when registration is attempted again, then the service returns “This username already exists” and does not create a duplicate account.
•	Invalid fields: Given a missing app_id, empty username, or password shorter than 12 characters, when registration is requested, then the service returns with an error and identifies the invalid field(s)

"""
print("================= USER STORY 1: Register a Personal Account =================\n\n")



print("-----------------------------------------------------------")

print("Functional Requirement 1 - Successfully Registering:\n\nGiven an app_id, an unused username, and a password of at least 12 characters,\nwhen the registration is sent,then the service returns “success” with a new\nuser_id, app_id, and username, without returning the password.\n")
print("Expected: 201")
send("/register", {"app_id":"medical_journal", "username":"matamory", "password":"password1234"})

print("-----------------------------------------------------------")

print("Functional Requirement 2 - Duplicate user attempt:\n\nGiven a username that is already registered within the same app_id,\nwhen registration is attempted again, then the service returns “This username already exists” \nand does not create a duplicate account.\n")
print("Expected: 409")
send("/register", {"app_id":"medical_journal", "username":"matamory", "password":"newpassword1234"})


print("-----------------------------------------------------------")

print("Functional Requirement 3 - Invalid Fields:\n\nGiven a missing app_id, empty username, or password shorter than 12 characters,\n when registration is requested, then the service returns with an error and identifies\n the invalid field(s)\n")
print("Expected: 400")
send("/register", {"username": "", "password":"pass"})


#========================== USER STORY 2 ========================== Login to an Existing Account
"""

•	Successful login: Given a registered app_id, username and correct password, when Login button is clicked, then the service returns “success” with a successful authentication result.
•	Invalid login: Given an incorrect password or a username that does not exist in that app_id, when the sign-in request is submitted, then the service returns “invalid credentials” and does not indicate the user

"""

print("================= USER STORY 2: Login to an Existing Account =================\n\n")


print("-----------------------------------------------------------")

print("Functional Requirement 1 - Successful login:\n\nGiven a registered app_id, username and correct password,\n when Login button is clicked, then the service returns “success” with a successful authentication result.\n")
print("Expected: 200")
send("/login", {"app_id":"medical_journal", "username":"matamory", "password":"password1234"})


print("-----------------------------------------------------------")

print("Functional Requirement 2 - Invalid login:\n\nGiven an incorrect password or a username that does not exist in that app_id,\n when the sign-in request is submitted, then the service returns “invalid credentials” and\n does not indicate the user\n")
print("Wrong Password- Expected: 401")
send("/login", {"app_id":"medical_journal", "username":"matamory", "password":"wrongpass"})


print("\n\nNonexistent username - Expected: 401")
send("/login", {"app_id":"medical_journal", "username":"randUser", "password":"password1234"})


#========================== USER STORY 3 ========================== Application-Specific Account
"""
•	Given a user has an existing Fitness Tracker account with a valid username and password, when the user submits those credentials to log in to Fitness Tracker, then the Login Microservice returns a successful authentication result.
•	Given a username and password are valid for Fitness Tracker but not for Medical Journal, when those credentials are submitted for Medical Journal, then the Login Microservice returns an unsuccessful authentication result.

"""


print("================= USER STORY 3: Application-Specific Login =================\n\n")


print("-----------------------------------------------------------")

print("Functional Requirement 1 - Successful app-specific login:\n\nGiven a user has an existing Fitness Tracker account with a valid username and password,\nwhen the user submits those credentials to log in to Fitness Tracker,\n then the Login Microservice returns a successful authentication result.\n")
print("Setup: create a Fitness Tracker account - Expected: 201")
send("/register", {"app_id":"fitness_tracker", "username":"yesenia", "password":"somepassword"})

print("Log in to Fitness Tracker - Expected: 200")
send("/login", {"app_id":"fitness_tracker", "username":"yesenia", "password":"somepassword"})


print("-----------------------------------------------------------")

print("Functional Requirement 2 - Cross-application login attempt:\n\nGiven a username and password are valid for Fitness Tracker but not for Medical Journal,\nwhen those credentials are submitted for Medical Journal, then the Login Microservice \nreturns an unsuccessful authentication result.\n")
print("Expected: 401")
send("/login", {"app_id":"medical_journal", "username":"yesenia", "password":"somepassword"})

