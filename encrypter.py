from cryptography.fernet import Fernet

# ----------------------------- Encryption  ----------------------------------

# cryptography needs authentication to word so we will 
# be authenticating it by generating a key which we will use 
# every time we ask it to encrypt something.

# generates a unique key, makes a new fule named pass.key in the currenct folder
# and stores the pass/authentication key in that file
def generateWriteKey():
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)

# gets the authentication key
def getKey():
    key = open("pass.key", "rb").read()
    return key

# encrypts message and returns it
def encryptSecret(secret):
    generateWriteKey()
    text = secret.encode()
    key = getKey()
    auth = Fernet(key)
    return auth.encrypt(text)

# decrypts message and retrurns message
def decryptSecret(encrypted):
    key = getKey()
    auth = Fernet(key)
    return auth.decrypt(encrypted)

# def test():
#     msg=input("Enter the message you want to ENCRYPT : ")
#     encrypted = encryptSecret(msg)
#     print(encrypted)
#     decrypted = decryptSecret(encrypted)
#     print(decrypted)
#     print(len(decrypted))

# test()
