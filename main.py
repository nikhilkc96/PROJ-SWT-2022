import hashlib
# pip install pyfiglet
import pyfiglet
import json
from pysondb import db

database=db.getDb("database.json")

ascii_banner = pyfiglet.figlet_format("A Digital Dating Service!!")
def signup():
    name = input("Please enter your name?: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender: ")
    interests = input("Enter your intersts: ")
    pre_gen = input("Enter the preferred gender to meet: ")
    email = input("Enter email address: ")
    pwd = input("Enter password: ")
    conf_pwd = input("Confirm password: ")
    if conf_pwd == pwd:
        enc = conf_pwd.encode()
        hash1 = hashlib.md5(enc).hexdigest()
        profiles = {
            'Name': name,
            'Age' : age, 
            'Gender': gender, 
            'Interstes': interests, 
            'Per_Gender': pre_gen,
            'Email': email,
            'PassWord': hash1
        } 
        database.add(profiles)
        print("You have registered successfully!")
    else:
        print("Password is not same as above! \n")
def login():
    database=db.getDb("database.json")
    email = input("Enter email: ")
    pwd = input("Enter password: ")
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    demo = database.getAll()
    output_dict = [x for x in demo if x['Email'] == email and x['PassWord'] == auth_hash]
    if any(output_dict):
         print("Logged in Successfully!")
    else:
         print("Login failed! \n")
while 1:
    
    print(ascii_banner)
    print("1.Signup")
    print("2.Login")
    print("3.Exit")
    print("*****************************")

    ch = int(input("Enter your choice: "))
    if ch == 1:
        signup()
    elif ch == 2:
        login()
    elif ch == 3:
        break
    else:
        print("Wrong Choice!")
