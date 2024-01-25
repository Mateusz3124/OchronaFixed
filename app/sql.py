from mysql.connector import pooling
from Crypto.Protocol.KDF import PBKDF2
import random
import secrets
import string
from passlib.hash import argon2
from hashlib import blake2b
from base64 import b64decode
from Crypto.Cipher import AES
from clearInput import clearInput
dbconfig = {
    "host": "172.17.0.1",
    "port": "3306",
    "user": "root",
    "password": "Jon15SgqPwkdaw1HKwwps1",
    "database": "bank"
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=4, **dbconfig)

def generateTenValues():
    condition = True    

    while(condition):
        condition = False
        randomNumbers = [(secrets.randbelow(30)) for i in range(10)]
        sortedNumbers = sorted(randomNumbers)
        holder = -1
        counter = 0

        for value in sortedNumbers:
            if value < 10:
                counter = counter + 1
            if holder + 1 == value or holder == value:
                condition = True
                continue
            else:
                holder = value

        if counter < 2:
            condition = True

    return sortedNumbers

def generatePasswords(givenPassword):
    sequences = []

    for i in range(10):
        sequences.append(generateTenValues())

    passwords = []

    for sequence in sequences:
        counter = 0
        password = ""
        for letter in givenPassword:
            if counter not in sequence:
                password += letter
            counter += 1
        passwords.append(password)

    h = []

    for i in range(len(passwords)):
        value = argon2.hash(passwords[i])
        h.append([value, sequences[i]])

    return h

def sendTransactionToDatabase(transaction):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    data = (transaction.FromAccount,)
    sql = """
    SELECT id, account 
    FROM users 
    Where username = %s"""
    cursor.execute(sql, data)
    idSender = cursor.fetchone()
    
    data = (transaction.Account,)
    sql = """
    SELECT id 
    FROM users 
    Where account = %s"""
    cursor.execute(sql, data)
    idRecipient = cursor.fetchone()

    if not idRecipient:
        return True
    if idRecipient[0] == idSender[0]:
        return True

    data = (transaction.Title,transaction.Amount, idSender[1], transaction.Account,transaction.Name,transaction.Surname,transaction.Adress, idSender[0])
    sql = """
    INSERT INTO transactions (title, amount, fromAccount, account, name, surname, address, idUsername) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql,data)
    database.commit()
    data = (transaction.Title,transaction.Amount,idSender[1],transaction.Account,transaction.Name,transaction.Surname,transaction.Adress, idRecipient[0])
    cursor.execute(sql,data)
    database.commit()
    
    cursor.close()
    database.close()
    
    return False

def getTransaction(user):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    data = (user,)
    sql = """
    SELECT transactions.* 
    FROM transactions 
    JOIN users ON transactions.idUsername = users.id 
    WHERE users.username = %s"""
    cursor.execute(sql,data)
    data = cursor.fetchall()

    cursor.close()
    database.close()

    for container in data:
        for item in container:
            if clearInput(item) in "":
                return ""
            
    return data

def blake(user,value):
    secretKey = b"BKgasdqw3#!@#412fuiu[][fdDAgafhu3424fsfds;''[54]"
    h = blake2b(digest_size=30, salt=user.encode(), key=secretKey)
    h.update(value.encode())
    p = h.hexdigest()
    return p

def getInfoAboutUser(user):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    data = (user,)
    sql = """
    SELECT amount, account
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,data)
    data = cursor.fetchone()

    cursor.close()
    database.close()

    for item in data:
        if clearInput(item) in "":
            return ""
        
    holder = data[0].split(",")
    expected = blake(user,holder[0])
    if expected != holder[1]:
        return ""
    
    return data

def getBalanceFromAccount(account):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    data = (account,)
    sql = """
    SELECT amount, username
    FROM users 
    WHERE account = %s"""
    cursor.execute(sql,data)
    data = cursor.fetchone()

    cursor.close()
    database.close()

    holder = data[0].split(",")
    expected = blake(data[1],holder[0])
    if expected != holder[1]:
        return ""
    
    return data

def setBalance(accountFrom, accountTarget, balanceFrom, balanceTarget, user, targetUser):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    value = str(balanceFrom) + "," + blake(user, str(balanceFrom))

    data = (value, accountFrom)
    sql = """
    Update users
    Set amount = %s 
    Where account = %s;"""
    cursor.execute(sql, data)
    database.commit()

    valueTarget = str(balanceTarget) + "," + blake(targetUser, str(balanceTarget))

    data = (valueTarget, accountTarget)
    sql = """
    Update users
    Set amount = %s 
    Where account = %s;"""
    cursor.execute(sql, data)
    database.commit()

    cursor.close()
    database.close()
    
def changePassword(username, password):
    database = connection_pool.get_connection()
    passwordsWithSequences = generatePasswords(password)
    cursor = database.cursor()

    data = (username,)
    sql = """
    SELECT id 
    FROM users 
    Where username = %s"""
    cursor.execute(sql, data)
    idUsername = cursor.fetchone()

    sql = """
    DELETE 
    FROM passwords 
    WHERE idUsername = %s"""
    cursor.execute(sql,idUsername)
    database.commit()
    cursor.close()

    for elem in passwordsWithSequences:
        cursor = database.cursor()     

        data = (elem[0], ",".join(str(num) for num in elem[1]), idUsername[0])
        sql = """
        INSERT INTO passwords (password, sequence, idUsername) 
        VALUES (%s, %s, %s);"""
        cursor.execute(sql,data)
        database.commit()
        cursor.close()
    
    cursor.close()
    database.close()

def generateRandomString(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for i in range(length))
    return random_string

def addPasswordLink(request, username):
    database = connection_pool.get_connection()
    cursor = database.cursor()
    hash = generateRandomString(15)
    value = blake(username, str(request.access_route[-1]))
    secretHash = value +":"+str(request.access_route[-1])    

    data = (hash, secretHash)
    sql = """
    INSERT INTO changePassword (idVerification, secretIdVerification)  
    VALUES (%s,%s);"""
    cursor.execute(sql, data)
    database.commit()

    cursor.close()
    database.close()
    return [hash,secretHash]

def GetPasswordLink():
    database = connection_pool.get_connection()
    cursor = database.cursor()

    sql = """
    SELECT *
    FROM changePassword"""
    cursor.execute(sql)
    hashes = cursor.fetchall()

    cursor.close()
    database.close()
    return hashes

def deletePasswordLink(hash):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    data = (hash,)
    sql = """
    DELETE 
    FROM changePassword 
    WHERE idVerification = %s"""
    cursor.execute(sql, data)
    database.commit()

    cursor.close()
    database.close()

def getEmail(username):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    data = (username,)
    sql = """
    SELECT email
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,data)
    email = cursor.fetchone()

    cursor.close()
    database.close()
    if len(email) == 0:
        return None
    return email[0]

def decrypt(ciphertext,key, mode):
  (ciphertext,  authTag, nonce) = ciphertext
  aes = AES.new(key,  mode, nonce)
  return(aes.decrypt_and_verify(ciphertext, authTag))

def read(key, data):
    devidedData = data.split(";")
    text = ()
    for item in devidedData:
        text += (b64decode(item),)

    res= decrypt(text,key,AES.MODE_GCM)
    return res.decode()

def getData(username):
    database = connection_pool.get_connection()
    cursor = database.cursor()
    data = (username,)
    sql = """
    SELECT card, idNumber
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,data)
    values = cursor.fetchone()
    cursor.close()
    database.close()
    card = values[0]
    id = values[1]
    key = PBKDF2(b"HGKTuwY11@!2"+username.encode(), b"PPGuvXffq")
    holder = []
    result = read(key,card)
    holder.append(result)
    result = read(key,id)
    holder.append(result)
    return holder

def loginWithUsername(username):
    sequences = []
    database = connection_pool.get_connection()
    cursor = database.cursor()

    data = (username,)
    sql = """
    SELECT passwords.sequence 
    FROM passwords 
    JOIN users ON passwords.idUsername = users.id 
    WHERE users.username = %s"""
    cursor.execute(sql,data)
    sequences = cursor.fetchall()

    cursor.close()
    database.close()
    return sequences

def loginWithPassword(username, password):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    data = (username,)
    sql = """
    SELECT loginCount
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,data)
    count = cursor.fetchone()

    if len(count) == 0:
        return True
    
    if count[0] >= 5:
        cursor.close()
        database.close()
        return None
    
    data = (username,)
    sql = """
    SELECT passwords.password 
    FROM passwords 
    JOIN users ON passwords.idUsername = users.id 
    WHERE users.username = %s"""
    cursor.execute(sql,data)
    passwords = cursor.fetchall()

    cursor.close()
    containtsPassword = False

    for passw in passwords:
        if argon2.verify(password, passw[0]):
            containtsPassword = True
            break

    if not containtsPassword:
        cursor = database.cursor()
        data = (username,)
        sql  = """
                       UPDATE users 
                       SET loginCount = loginCount + 1 
                       WHERE username = %s"""
        cursor.execute(sql,data)
        database.commit()

    else:
        cursor = database.cursor()
        data = (username,)
        sql  = """
                       UPDATE users 
                       SET loginCount = 0 
                       WHERE username = %s"""
        cursor.execute(sql,data)
        database.commit()

    cursor.close()
    database.close()
    return not containtsPassword
