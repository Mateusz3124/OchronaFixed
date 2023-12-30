from flask import Flask, render_template, request, make_response, redirect, url_for
import mysql.connector 
from mysql.connector import pooling
import random
from passlib.hash import argon2
import time
import re

dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "root",
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
    if count[0][0] == 5:
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
    cursor.close()
    database.close()
    return containtsPassword
