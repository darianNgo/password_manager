import string
import secrets
import random
import psycopg2
import getpass
from cryptography.fernet import Fernet
import encrypter

# ----------------------------- Authentication  ---------------------------

# connects to data base and authenticates user and returns connection
def connectDataBase():
    user = input("Enter username: ")
    password = getpass.getpass("Enter Password: ") # TODO: password currently doesnt work
    connection = None

    try:
        connection = psycopg2.connect(database="passwords", user=user, password=password, host='127.0.0.1', port='5432')
        if connection is not None:
            print('Connection established')
        else:
            print('Connection not established')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return connection

# print(connectDataBase()) # testing
        
# ----------------------------- Functionalities  ---------------------------

# find passwords by username or URL and prints all columns of table
def findPassword(passwords):
    print("How would you like to find your password?")
    print("By username: 0, By URL: 1")
    method = int(input("Method: "))
    searchBy = ""
    if method == 0:
        searchBy = input("Enter username: ")
    elif method == 1:
        searchBy = input("Enter URL: ")
    else:
        print("an error occured: invalid input")
        return

    count = 0

    for row in passwords:
        if row[method] == searchBy:
            count+=1
            print(count, ":")
            print("username: ", row[0])
            print("URL:      ", row[1])
            print("password: ", row[2])
    
    if count == 0:
        if method == 0:
            print("No passwords found by username: ", searchBy)
        else:
            print("No passwords found by URL: ", searchBy)


# findPassword(connectDataBase()) # testing

# retreives all entries from table and returns them
def getAccounts(connection):
    cursor = connection.cursor()
    query = "select * from accounts"
    cursor.execute(query)
    return cursor.fetchall()


# closes the current connection to db
def closeConnection(connection):
    connection.close()
    print("Connection closed")

def savePassword(username, url, password, connection):
    cursor = connection.cursor()
    cursor.execute("insert into accounts (username, url, password) values(%s, %s, %s)", (username, url, password))
    print("Password for username = " + username + " at URL = " + url + " was successfully saved")



# ----------------------------- Password Generator ---------------------------

# generates a new password using secrets random generator
def passwordGenerator(length):
    # all character choices: uppercase, lowercase, special characters, and numbers
    characters = list(string.ascii_uppercase) + list(string.ascii_lowercase) + list('0123456789') + list('!@#$%^&*()-_+=?:{[]}.')
    # shuffle the list
    random.shuffle(characters)
    password = ''
    # chooses a secret random choice in the shuffled characters list and append to the password
    for i in range(length):
        password += secrets.choice(seq=characters)
    return password

# testing
# print(passwordGenerator(25))

