import hashlib
# import pyfiglet
import json
from pysondb import db
import getpass
from os import path
import pandas as pd
from fuzzywuzzy import fuzz
#from goto import with_goto


path_to_dat = path.abspath(path.join(path.dirname(__file__), 'database.json'))
# print(path_to_dat)
database=db.getDb(path_to_dat)

# ascii_banner = pyfiglet.figlet_format("A Digital Dating Service!!")

def signup():
    name = input("Please enter your name?: ")
    age = input("Enter your age: ")
    while not age.isdigit():
            print("That's not a correct number. Try again.")
            age = input("Enter your choice: ")
    gender= input("What is your gender? \nEnter 'M' for Male or 'F' for Female\n").upper()
    if gender == "M":
        gender = "Male"
    elif gender == "F":
        gender= "Female"
    else:
        print("Wrong Choice!")    
        signup()
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
         print("Login failed! (Enter the correct email and password)\n")



def match(x):
    print("Logged in Successfully!")
    print("\nYour Profile Details:\n")
    df = pd.DataFrame(x)
    print(df[['id','Name','Age','Gender','Per_Gender','Interstes','Email']]) 
    
    

    while 1:
        print("\n1.Find Your Match")
        print("2.View all Profiles")
        print("3.Exit")
        print("*****************************")
        answer = input("Enter your choice: ")
        while not answer.isdigit():
            print("That's not a correct number choice. Try again.")
            answer = input("Enter your choice: ")
        ch = int(answer)
        if ch == 1:
            print("\nYour Match: \n") 
            df = pd.DataFrame(x)
            perf =  df['Per_Gender'].values[0]
            intu =  df['Interstes'].values[0]
            gender_match = database.reSearch("Gender", perf)
            # print(gender_match)
            gender_match_dic = pd.DataFrame(gender_match)
            print ("{:<20} {:<10} {:<10} {:<10} {:<22} {:<30} {:<1}".format('Name','Age','Gender','Per_Gender','Email','Intersts','Match %'))
            for Name, Age, Gender, Per_Gender, Email, Interstes in zip(gender_match_dic['Name'], gender_match_dic['Age'],gender_match_dic['Gender'],gender_match_dic['Per_Gender'],gender_match_dic['Email'],gender_match_dic['Interstes']):
                print ("{:<20} {:<10} {:<10} {:<10} {:<22} {:<30} {:<1}".format(Name, Age, Gender, Per_Gender, Email,Interstes,fuzz.ratio(Interstes,intu),"%"))
        elif ch == 2:
            a = database.getAll()
            df = pd.DataFrame(a)
            print(df[['id','Name','Age','Gender','Per_Gender','Interstes','Email']])
        elif ch == 3:
            break
        else:
            print("Wrong Choice!")
    

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
    answer = input("Enter your choice: ")
    while not answer.isdigit():
        print("That's not a number. Try again.")
        answer = input("Enter your choice: ")
    ch = int(answer)
    if ch == 1:
        signup()
    elif ch == 2:
        login()
    elif ch == 3:
        break
    else:
        print("Wrong Choice!")
