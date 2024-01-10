from flask import render_template, request, make_response, redirect, url_for
from mysql.connector import pooling
from Crypto.Protocol.KDF import PBKDF2
import random
import secrets
import string
from passlib.hash import argon2
from base64 import b64decode
from Crypto.Cipher import AES
import time
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
        random.seed(time.perf_counter())
        randomNumbers = [random.randint(1, 30) for i in range(8)]
        sortedNumbers = sorted(randomNumbers)
        holder = -1
        for value in sortedNumbers:
            if holder + 1 == value or holder == value:
                condition = True
                continue
            else:
                holder = value
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
    Sender = cursor.fetchall()
    
    data = (transaction.Account,)
    sql = """
    SELECT id 
    FROM users 
    Where account = %s"""
    cursor.execute(sql, data)
    idRecipientUsername = cursor.fetchall()

    if not idRecipientUsername:
        return True
    
    if idRecipientUsername[0][0] == Sender[0][0]:
        return True

    data = (transaction.Title,transaction.Amount, Sender[0][1], transaction.Account,transaction.Name,transaction.Surname,transaction.Adress, Sender[0][0])
    sql = """
    INSERT INTO transactions (title, amount, fromAccount, account, name, surname, address, idUsername) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql,data)
    database.commit()
    data = (transaction.Title,transaction.Amount,Sender[0][1],transaction.Account,transaction.Name,transaction.Surname,transaction.Adress, idRecipientUsername[0][0])
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
    return data

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
    idUsername = cursor.fetchall()
    sql = """
    DELETE 
    FROM passwords 
    WHERE idUsername = %s"""
    cursor.execute(sql,idUsername[0])
    database.commit()
    cursor.close()
    for elem in passwordsWithSequences:
        cursor = database.cursor()     
        data = (elem[0], ",".join(str(num) for num in elem[1]), idUsername[0][0])
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

def addPasswordLink():
    database = connection_pool.get_connection()
    cursor = database.cursor()
    hash = generateRandomString(15)  
    data = (hash,)
    sql = """
    INSERT INTO changePassword (idVerification)  
    VALUES (%s);"""
    cursor.execute(sql, data)
    database.commit()
    cursor.close()
    database.close()
    return hash

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


def decrypt(data,key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = aes.decrypt(data)
    return encrypted_data

def read(key, data):
    block = []

    data = data.split(";")
    iv = b64decode(data[0])
    data = b64decode(data[1])

    for i in range(int(len(data)/16)):
        block.append(data[i*16 : i*16 + 16])

    result = []

    result.append(decrypt(block[0], key, iv))

    for i in range(len(block)-1):
        result.append(decrypt(block[i+1], key, block[i]))
    data = b"".join(result)
    data = data.rstrip(b"\x00")
    return data.decode()

def getData(username):
    database = connection_pool.get_connection()
    cursor = database.cursor()
    data = (username,)
    sql = """
    SELECT card, idNumber
    FROM users 
    WHERE username = %s"""
    cursor.execute(sql,data)
    values = cursor.fetchall()
    cursor.close()
    database.close()
    card = values[0][0]
    id = values[0][1]
    key = PBKDF2(b"HGKTuwY11@!2"+username.encode(), b"PPGuvXffq")
    holder = []
    result = read(key,card)
    holder.append(result)
    result = read(key,id)
    holder.append(result)
    return holder

def loginWithUsernameMethod(username):
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

def loginWithUsername(username):
    sequences = []
    sequences = loginWithUsernameMethod(username)
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
    count = cursor.fetchall()
    if count[0][0] >= 5:
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
    containtsPassword = True
    for passw in passwords:
        if argon2.verify(password, passw[0]):
            containtsPassword = False
    if containtsPassword:
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
    return containtsPassword
