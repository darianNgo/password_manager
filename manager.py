import string
import secrets
import random
import psycopg2
import getpass
from cryptography.fernet import Fernet
import encrypter

# ----------------------------- Connection  ---------------------------

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

# closes the current connection to db
def closeConnection(connection):
    connection.close()
    print("Connection closed")

        
# ----------------------------- Functionalities  ---------------------------

# find passwords by username or URL and prints all columns of table
def findPassword(connection):
    # get the user input on whether to search for the password via url or username
    print("How would you like to find your password?")
    print("By username: 0, By URL: 1")
    method = int(input("Method: "))
    searchBy = ""
    passwords = None
    cursor = connection.cursor()

    # executes SQL command given the input and stores search results in the passwords variable
    if method == 0:
        searchBy = input("Enter username: ")
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (searchBy,))
        passwords = cursor.fetchall()
    elif method == 1:
        searchBy = input("Enter URL: ")
        cursor.execute("SELECT * FROM accounts WHERE url = %s", (searchBy,))
        passwords = cursor.fetchall()
    else:
        print("an error occured: invalid input")
        return
    
    findby = "username" if method == 0 else "url"
    print(len(passwords), "password found by ", findby, "=", searchBy)

    count = 0
    for row in passwords:
        count+=1
        print(count, ":")
        print("     username: ", row[0])
        print("     URL:      ", row[1])
        print("     password: ", encrypter.decryptSecret(row[2]))


# findPassword(connectDataBase()) # testing

# retreives all entries from table and returns them
def getAllAccounts(connection):
    cursor = connection.cursor()
    query = "select * from accounts"
    cursor.execute(query)
    passwords = cursor.fetchall()
    count = 0
    if passwords == None:
        print("No passwords found")
    else:
        print("\nHere are the passwords that were previously saved:\n")
        for row in passwords:
            count+=1
            print(count, ":")
            print("     username:  ", row[0])
            print("     URL:       ", row[1])
            print("     password:  ", encrypter.decryptSecret(row[2]))

# returns the number of entries
def getNumberOfAccounts(connection):
    cursor = connection.cursor()
    query = "select * from accounts"
    cursor.execute(query)
    passwords = cursor.fetchall()
    count = 0
    for row in passwords:
        count+=1
    return count

     

# saves the username, url, and password to the db
def savePassword(username, url, password, connection):
    cursor = connection.cursor()
    encryptedPass = encrypter.encryptSecret(password)
    cursor.execute("INSERT INTO accounts (username, url, password) VALUES(%s, %s, %s)", (username, url, encryptedPass))
    connection.commit()
    print("Password for username = " + username + " at URL = " + url + " was successfully SAVED")

def deletePassword(username, url, connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM accounts WHERE username = %s AND url = %s", (username, url))
    connection.commit()
    print("Password for username = " + username + " at URL = " + url + " was successfully DELETED")

def updatePassword(username, url, newPassword, connection):
    cursor = connection.cursor()
    encryptedPass = encrypter.encryptSecret(newPassword)
    cursor.execute("UPDATE accounts SET password = %s WHERE username = %s AND url = %s", (encryptedPass, username, url))
    connection.commit()
    print("Password for username = " + username + " at URL = " + url + " was successfully UPDATED")



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

