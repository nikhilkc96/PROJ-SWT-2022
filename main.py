import hashlib
# import pyfiglet
import json
from pysondb import db
import getpass
from os import path
import pandas as pd
from fuzzywuzzy import fuzz
# from fuzzywuzzy import process


path_to_dat = path.abspath(path.join(path.dirname(__file__), 'database.json'))
# print(path_to_dat)
database=db.getDb(path_to_dat)

# ascii_banner = pyfiglet.figlet_format("A Digital Dating Service!!")

def signup():
    name = input("Please enter your name?: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender: ")
    interests = input("Enter your intersts: ")
    pre_gen = input("Enter the preferred gender to meet: ")
    email = input("Enter email address: ")
    pwd = getpass.getpass('Enter Password: ')
    conf_pwd = getpass.getpass('Confirm password:')
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
    database=db.getDb(path_to_dat)
    email = input("Enter email: ")
    pwd = getpass.getpass('Enter Password: ')
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
    print("\nYour Profile Details:\n")
    df = pd.DataFrame(x)
    print(df[['id','Name','Age','Gender','Per_Gender','Interstes','Email']]) 

    print("\nYour Match: \n") 
    perf =  df['Per_Gender'].values[0]
    intu =  df['Interstes'].values[0]
    gender_match = database.reSearch("Gender", perf)
    gender_match_dic = pd.DataFrame(gender_match)
    print ("{:<10} {:<10} {:<10} {:<10} {:<20} {:<1}".format('Name','Age','Gender','Per_Gender','Email','Interstes'))
    for Name, Age, Gender, Per_Gender, Email, Interstes in zip(df['Name'], df['Age'],df['Gender'],df['Per_Gender'],df['Email'],df['Interstes']):
        print ("{:<10} {:<10} {:<10} {:<10} {:<20} {:<1} {:<1}".format(Name, Age, Gender, Per_Gender, Email, fuzz.ratio(Interstes,intu),"%"))
    
    # print(gender_match_dic[['Name','Age','Gender','Per_Gender','Email']])
    

while 1:
    
    # print(ascii_banner)
    print("""
    _      ____  _       _ _        _   ____        _   _             
   / \    |  _ \(_) __ _(_) |_ __ _| | |  _ \  __ _| |_(_)_ __   __ _ 
  / _ \   | | | | |/ _` | | __/ _` | | | | | |/ _` | __| | '_ \ / _` |
 / ___ \  | |_| | | (_| | | || (_| | | | |_| | (_| | |_| | | | | (_| |
/_/   \_\ |____/|_|\__, |_|\__\__,_|_| |____/ \__,_|\__|_|_| |_|\__, |
                   |___/                                        |___/ 
 ____                  _          _ _ 
/ ___|  ___ _ ____   _(_) ___ ___| | |
\___ \ / _ \ '__\ \ / / |/ __/ _ \ | |
 ___) |  __/ |   \ V /| | (_|  __/_|_|
|____/ \___|_|    \_/ |_|\___\___(_|_)
    """)
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
