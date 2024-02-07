from mysql.connector import pooling
from Crypto.Protocol.KDF import PBKDF2
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
    generatingSequence = True    

    while generatingSequence:
        generatingSequence = False
        randomNumbers = [(secrets.randbelow(30)) for i in range(10)]
        sortedNumbers = sorted(randomNumbers)
        previousNumber = -1
        numberOfElementsBelowTen = 0

        for value in sortedNumbers:
            if value < 10:
                numberOfElementsBelowTen = numberOfElementsBelowTen + 1
            if previousNumber + 1 == value or previousNumber == value:
                generatingSequence = True
                continue
            else:
                previousNumber = value

        if numberOfElementsBelowTen < 2:
            generatingSequence = True

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

    val = (transaction.FromAccount,)
    sql = """
    SELECT id, account 
    FROM users 
    Where username = %s"""
    cursor.execute(sql, val)
    dataSender = cursor.fetchone()
    
    val = (transaction.Account,)
    sql = """
    SELECT id 
    FROM users 
    Where account = %s"""
    cursor.execute(sql, val)
    dataRecipient = cursor.fetchone()

    if not dataRecipient:
        return True
    if dataRecipient[0] == dataSender[0]:
        return True

    val = (transaction.Title,transaction.Amount, dataSender[1], transaction.Account,transaction.Name,transaction.Surname,transaction.Adress, dataSender[0])
    sql = """
    INSERT INTO transactions (title, amount, fromAccount, account, name, surname, address, idUsername) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql,val)
    database.commit()
    val = (transaction.Title,transaction.Amount,dataSender[1],transaction.Account,transaction.Name,transaction.Surname,transaction.Adress, dataRecipient[0])
    cursor.execute(sql,val)
    database.commit()
    
    cursor.close()
    database.close()
    
    return False

def getTransaction(user):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    val = (user,)
    sql = """
    SELECT transactions.* 
    FROM transactions 
    JOIN users ON transactions.idUsername = users.id 
    WHERE users.username = %s"""
    cursor.execute(sql,val)
    transactions = cursor.fetchall()

    cursor.close()
    database.close()

    for container in transactions:
        for item in container:
            if clearInput(item) in "":
                return ""
            
    return transactions

def blake(user,value):
    secretKey = b"BKgasdqw3#!@#412fuiu[][fdDAgafhu3424fsfds;''[54]"
    h = blake2b(digest_size=30, salt=user.encode(), key=secretKey)
    h.update(value.encode())
    p = h.hexdigest()
    return p

def getInfoAboutUser(user):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    val = (user,)
    sql = """
    SELECT amount, account
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,val)
    dataUser = cursor.fetchone()

    cursor.close()
    database.close()

    for item in dataUser:
        if clearInput(item) in "":
            return ""
        
    holder = dataUser[0].split(",")
    expected = blake(user,holder[0])
    if expected != holder[1]:
        return ""
    
    return dataUser

def getBalanceFromAccount(account):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    val = (account,)
    sql = """
    SELECT amount, username
    FROM users 
    WHERE account = %s"""
    cursor.execute(sql,val)
    dataAboutAccount = cursor.fetchone()

    cursor.close()
    database.close()

    holder = dataAboutAccount[0].split(",")
    expected = blake(dataAboutAccount[1],holder[0])
    if expected != holder[1]:
        return ""
    
    return dataAboutAccount

def setBalance(accountFrom, accountTarget, balanceFrom, balanceTarget, user, targetUser):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    value = str(balanceFrom) + "," + blake(user, str(balanceFrom))

    val = (value, accountFrom)
    sql = """
    Update users
    Set amount = %s 
    Where account = %s;"""
    cursor.execute(sql, val)
    database.commit()

    valueTarget = str(balanceTarget) + "," + blake(targetUser, str(balanceTarget))

    val = (valueTarget, accountTarget)
    sql = """
    Update users
    Set amount = %s 
    Where account = %s;"""
    cursor.execute(sql, val)
    database.commit()

    cursor.close()
    database.close()
    
def changePassword(username, password):
    database = connection_pool.get_connection()
    passwordsWithSequences = generatePasswords(password)
    cursor = database.cursor()
    
    val = (username,)
    sql = """
    SELECT id 
    FROM users 
    Where username = %s"""
    cursor.execute(sql, val)
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

        val = (elem[0], ",".join(str(num) for num in elem[1]), idUsername[0])
        sql = """
        INSERT INTO passwords (password, sequence, idUsername) 
        VALUES (%s, %s, %s);"""
        cursor.execute(sql,val)
        database.commit()
        cursor.close()
    
    cursor.close()
    database.close()

def generateRandomString(length):
    characters = string.ascii_letters + string.digits
    randomString = ''.join(secrets.choice(characters) for i in range(length))
    return randomString

def addPasswordLink(request, username):
    database = connection_pool.get_connection()
    cursor = database.cursor()
    hashWebsiteUrl = generateRandomString(15)
    value = blake(username, str(request.access_route[-1]))
    hashCookie = value +":"+str(request.access_route[-1])    

    val = (hashWebsiteUrl, hashCookie)
    sql = """
    INSERT INTO changePassword (idVerification, secretIdVerification)  
    VALUES (%s,%s);"""
    cursor.execute(sql, val)
    database.commit()

    cursor.close()
    database.close()
    return [hashWebsiteUrl,hashCookie]

def GetPasswordLink():
    database = connection_pool.get_connection()
    cursor = database.cursor()

    sql = """
    SELECT *
    FROM changePassword"""
    cursor.execute(sql)
    links = cursor.fetchall()

    cursor.close()
    database.close()
    return links

def deletePasswordLink(hash):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    val = (hash,)
    sql = """
    DELETE 
    FROM changePassword 
    WHERE idVerification = %s"""
    cursor.execute(sql, val)
    database.commit()

    cursor.close()
    database.close()

def getEmail(username):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    val = (username,)
    sql = """
    SELECT email
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,val)
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

def getPersonalData(username):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    val = (username,)
    sql = """
    SELECT card, idNumber
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,val)

    values = cursor.fetchone()
    cursor.close()
    database.close()

    card = values[0]
    id = values[1]
    key = PBKDF2(b"HGKTuwY11@!2"+username.encode(), b"PPGuvXffq")
    personalData = []
    result = read(key,card)
    personalData.append(result)
    result = read(key,id)
    personalData.append(result)
    return personalData

def loginWithUsername(username):
    sequences = []
    database = connection_pool.get_connection()
    cursor = database.cursor()

    val = (username,)
    sql = """
    SELECT passwords.sequence 
    FROM passwords 
    JOIN users ON passwords.idUsername = users.id 
    WHERE users.username = %s"""
    cursor.execute(sql,val)
    sequences = cursor.fetchall()

    val = (username,)
    sql = """
    SELECT currentSequence 
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,val)
    currentSequence = cursor.fetchone()

    cursor.close()
    database.close()
    return sequences, currentSequence

def loginWithPassword(username, password):
    database = connection_pool.get_connection()
    cursor = database.cursor()

    val = (username,)
    sql = """
    SELECT loginCount
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,val)
    countOfFailedLogins = cursor.fetchone()

    if len(countOfFailedLogins) == 0:
        return True
    
    if countOfFailedLogins[0] >= 5:
        cursor.close()
        database.close()
        return None
    
    val = (username,)
    sql = """
    SELECT passwords.password 
    FROM passwords 
    JOIN users ON passwords.idUsername = users.id 
    WHERE users.username = %s"""
    cursor.execute(sql,val)
    passwords = cursor.fetchall()

    cursor.close()
    containtsPassword = False

    for passw in passwords:
        if argon2.verify(password, passw[0]):
            containtsPassword = True
            break

    if not containtsPassword:
        cursor = database.cursor()
        val = (username,)
        sql  = """
                       UPDATE users 
                       SET loginCount = loginCount + 1 
                       WHERE username = %s"""
        cursor.execute(sql,val)
        database.commit()

    else:
        cursor = database.cursor()
        val = (username,)
        sql  = """
                       UPDATE users 
                       SET loginCount = 0 
                       WHERE username = %s"""
        cursor.execute(sql,val)
        database.commit()

    cursor.close()
    database.close()
    return not containtsPassword

def changeCurrentSequence(username):
    database = connection_pool.get_connection()
    cursor = database.cursor()
    random = secrets.randbelow(10)
    val = (random, username)
    sql = """
    UPDATE users
    SET currentSequence = %s
    WHERE users.username = %s"""
    cursor.execute(sql,val)
    database.commit()

    cursor.close()
    database.close()
    return