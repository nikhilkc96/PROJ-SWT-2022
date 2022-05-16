import hashlib
# import pyfiglet
import json
from pysondb import db
import getpass
from os import path
import pandas as pd
from fuzzywuzzy import fuzz
import re


# path_to_dat = path.abspath(path.join(path.dirname(file), 'database.json'))
# print(path_to_dat)
database=db.getDb("database.json")

# ascii_banner = pyfiglet.figlet_format("A Digital Dating Service!!")

def printHeader(title):
    print(title)
    print("================")


# ==================
# ==== Validation

def readInput(field, validators, inputMessage="", errorMessage="", getInput = input):
    x = getInput("Enter your " + field + ": ") if inputMessage == "" else getInput(inputMessage)
    if not all(v(x) for v in validators):
        print("Invaid " + field + ". Try again!") if errorMessage == "" else print(errorMessage)
        return readInput(field, validators, inputMessage, errorMessage, getInput)
    return x

def isRequired(x):
    return x != "" and x != None

def isNumeric(x):
    return x.isdigit() or x == ""

def isValidEmail(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    if email_regex.match(email):
        return True
    return False

def isOneOf(xs):
    return lambda x: x in xs

def isEqual(s):
    return lambda x: x == s

# =================

def signup():
    printHeader("Sign Up")
    name = readInput("name", [isRequired])
    age = readInput("age", [isRequired, isNumeric])
    gender = readInput("gender", [isRequired, isOneOf(["M", "F"])]
                       , inputMessage="What is your gender (Enter 'M' for Male or 'F' for Female): ")
    interests = readInput("interests", [isRequired])
    pre_gen = readInput("gender", [isRequired, isOneOf(["M", "F"])]
                        , inputMessage="Enter the preferred gender to meet: (Enter 'M' for Male or 'F' for Female): ")
    email = readInput("email", [isRequired, isValidEmail])
    pwd = readInput("password", [isRequired], getInput=getpass.getpass)
    conf_pwd = readInput("confirm password", [isRequired, isEqual(pwd)], getInput=getpass.getpass, inputMessage="Confirm password: ")

    gender = "Male" if gender == "M" else "Female"
    pre_gen = "Male" if pre_gen == "M" else "Female"

    # Check if email is already exists
    if database.getByQuery({"Email": email}):
        print("User with email \"" + email + "\" is already exists.")
        return

    enc = conf_pwd.encode()
    hash1 = hashlib.md5(enc).hexdigest()
    profile = {
        'Name': name,
        'Age' : age,
        'Gender': gender,
        'Interstes': interests,
        'Per_Gender': pre_gen,
        'Email': email,
        'PassWord': hash1
    }

    print("\nYour Profile")
    print("===============")
    print("Name:", name)
    print("Email:", email)
    print("Age:", age)
    print("Gender:", gender)
    print("Interests:", interests)
    print("Per Gender:", pre_gen)

    database.add(profile)
    print("You have registered successfully!")

def login():
    printHeader("Login")
    email = readInput("email", [isRequired, isValidEmail])
    pwd = readInput("password", [isRequired], getInput=getpass.getpass)
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()

    user = database.getByQuery({"Email": email, "PassWord": auth_hash})
    if user:
         print("Logged in Successfully!")
         print("\nYour Profile Details:\n")
         df = pd.DataFrame(user)
         print(df[['id','Name','Age','Gender','Per_Gender','Interstes','Email']]) 
         match(email)
    else:
         print("Login failed! (Enter the correct email and password)\n")

def match(email):
    x = database.getByQuery({"Email": email})
    print("\n1.Find Your Match")
    print("2.View all Profiles")
    print("3.View your Profile")
    print("4.Edit your Profile")
    print("5.Exit")
    print("*********")
    answer = int(readInput("choice", [isRequired, isOneOf(["1", "2", "3", "4", "5"])]))
    if answer == 1:
        print("\nYour Match: \n") 
        df = pd.DataFrame(x)
        perf =  df['Per_Gender'].values[0]
        intu =  df['Interstes'].values[0]
        gender_match = database.getByQuery({"Gender": perf})
        gender_match_dic = pd.DataFrame(gender_match)
        if not gender_match_dic.empty:
            print ("{:<10} {:<10} {:<10} {:<10} {:<20} {:<1}".format('Name','Age','Gender','Per_Gender','Email','Interstes'))
            for Name, Age, Gender, Per_Gender, Email, Interstes in zip(gender_match_dic['Name'], gender_match_dic['Age'],gender_match_dic['Gender'],gender_match_dic['Per_Gender'],gender_match_dic['Email'],gender_match_dic['Interstes']):
                print ("{:<10} {:<10} {:<10} {:<10} {:<20} {:<1} {:<1}".format(Name, Age, Gender, Per_Gender, Email, fuzz.ratio(Interstes,intu),"%"))

        match(email)
    elif answer == 2:
        a = database.getAll()
        df = pd.DataFrame(a)
        print(df)
        match(email)
    elif answer == 3:
        print("\nYour Profile Details:\n")
        df = pd.DataFrame(x)
        print(df[['id','Name','Age','Gender','Per_Gender','Interstes','Email']]) 
        match(email)
    elif answer == 4:
        editProfile(email)
        match(email)

def editProfile(email):
    user = database.getByQuery({"Email": email})[0]
    printHeader("Edit Profile")
    name = readInput("name", [], inputMessage="Enter new name (Leave empty if you dont want to change): ")
    age = readInput("age", [isNumeric], inputMessage="Enter new age (Leave empty if you dont want to change): ")
    interests = readInput("interests", [], inputMessage="Enter new interests (Leave empty if you dont want to change): ")

    database.updateByQuery({"Email": user["Email"]}
                         , {"Name": name or user["Name"], "Age": age or user["Age"], "Interstes": interests or user["Interstes"]})
    print("You account have updated successfully!")

def main():
    print("1.Signup")
    print("2.Login")
    print("3.Exit")
    print("*********")
    answer = int(readInput("choice", [isRequired, isOneOf(["1", "2", "3"])]))
    if answer == 1:
        signup()
        main()
    elif answer == 2:
        login()
        main()

main()
