import hashlib
# pip install pyfiglet
import pyfiglet
import json
from pysondb import db
import getpass
import pyautogui

database=db.getDb("database.json")

ascii_banner = pyfiglet.figlet_format("A Digital Dating Service!!")
def signup():
    name = input("Please enter your name?: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender: ")
    interests = input("Enter your intersts: ")
    pre_gen = input("Enter the preferred gender to meet: ")
    email = input("Enter email address: ")
    pwd = pyautogui.password(text='Enter Password', title='Password', default='', mask='*')
    conf_pwd = pyautogui.password(text='Confirm password:', title='Password', default='', mask='*')
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
    pwd = pyautogui.password(text='Enter Password', title='Password', default='', mask='*')
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    demo = database.getAll()
    output_dict = [x for x in demo if x['Email'] == email and x['PassWord'] == auth_hash]
    if any(output_dict):
         match(output_dict)
    else:
         print("Login failed! \n")



def match(x):
    print("Logged in Successfully!")
    print(x)

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
