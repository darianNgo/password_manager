import manager
import encrypter

# main function to call to start the password manager on terminal
def main():
    # authenticate user and establish a connection to the db
    connection = None
    while connection is None:
        print("Please authenticate!")
        connection = manager.connectDataBase()
        if connection == None:
            print("would you like to try again?")
            answer = input("y / n")
            if answer == "n":
                return
    # generates a new key to access password if it is the users first time using the system
    if manager.getNumberOfAccounts(connection) == 0:
        print("\n Is this the first time using the Password Manager? (y/n)")
        check = input()
        if check == "y":
            encrypter.generateWriteKey()
            print("New encryption key generated!")
    
    cont = "y"
    while cont == "y":
        mainMenu(connection)
        cont = input("\nIs there more I can do for you? (y/n)\n")
    
    if connection is not None:
        print("Good Bye!")
        manager.closeConnection(connection)

# gets the option of the user and returns it
def getUserOption():
    print("\nwhat would you like to do today?\n")
    print("     1: generate new password for an account")
    print("     2: find passwords")
    print("     3: view all currently saved passwords")
    print("     4: manage passwords (edit | delete | add)")
    print("     5: quit")
    return input()

# function that directs the user to the deisred functionality 
def mainMenu(connection):
    userOption = int(getUserOption())
    if userOption == 1:
        createPassword(connection)
    elif userOption == 2:
        manager.findPassword(connection)
    elif userOption == 3:
        manager.getAllAccounts(connection)
    elif userOption == 4:
        managePasswords(connection)
    elif userOption == 5:
        print("Good Bye!")
        manager.closeConnection()
        return
    else:
        print("Error: invalid Input. Please try again")
        mainMenu(connection)

# makes calls to functions that manages the users passwords, such as
# updating, deleting, and adding an existing password
def managePasswords(connection):
    print("\nPlease select one of the following options:\n")
    print("     1: Edit existing password")
    print("     2: Delete a password")
    print("     3: Add a password")
    print("     4: quit")
    option = int(input())
    if option < 1 or option > 4:
        print("Error: invalid input")
        return
    print(("\nPlease provide the following information:\n"))
    username = input("username: ")
    url =      input("URL: ")
    if option == 1:
        newPassword = input("new Password: ")
        manager.updatePassword(username, url, newPassword, connection)
    elif option == 2:
        print("\nAre you sure you would like to delete the password for username: " + username, "at URL: " + url + "? (y/n)")
        check = input()
        if check == "y":
            manager.deletePassword(username, url, connection)
        else:
            return
    elif option == 3:
        password = input("password: ")
        manager.savePassword(username, url, password, connection)
    else:
        return
    
# calls functions to generate a new secure password. 
# Makes sure the user is satified with the password generated before encrypting and saving it
# if the user is not satisfied, this function calls itself again and repeats the process
def createPassword(connection):
    length = input("\nPlease specify the number of characters you would like your password to be: \n")
    if not length.isnumeric():
        print("Invalid Input:", length, "is not a number")
        return
    else:
        length = int(length)
        password = manager.passwordGenerator(length)
        print("password =", password)
        option = input("\nwould you like to save this password? (y/n)\n")
        if option == "y":
            print(("\nPlease provide the following information to be saved:\n"))
            username = input("Enter username: ")
            url = input("Enter URL: ")
            manager.savePassword(username, url, password, connection)
        elif option == "n":
            option = input(("\nWould you like me to try again? (y/n)\n"))
            if option == "y":
                createPassword(connection)
            else:
                return
        else:
            print("Error: invalid input")
            return
    
    return

main()
