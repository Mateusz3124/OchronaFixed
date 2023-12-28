from flask import Flask, render_template, request, make_response, redirect, url_for
import mysql.connector
import random
from passlib.hash import argon2
import time
import re

database = mysql.connector.connect(host='localhost',user='root',passwd='root',database='bank')

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

def getTransaction(user):
    cursor = database.cursor()
    data = (user,)
    sql = """SELECT transactions.* FROM transactions JOIN users ON transactions.idUsername = users.id WHERE users.username = %s"""
    cursor.execute(sql,data)
    data = cursor.fetchall()
    cursor.close()
    return data

def changePassword(username, password):
    passwordsWithSequences = generatePasswords(password)
    cursor = database.cursor()
    data = (username,)
    sql = """SELECT id FROM users Where username = %s"""
    cursor.execute(sql, data)
    idUsername = cursor.fetchall()

    sql = """DELETE FROM passwords WHERE idUsername = %s"""
    cursor.execute(sql,idUsername[0])
    database.commit()

    for elem in passwordsWithSequences:     
        data = (elem[0], ",".join(str(num) for num in elem[1]), idUsername[0][0])
        sql = """INSERT INTO passwords (password, sequence, idUsername) VALUES (%s, %s, %s);"""
        cursor.execute(sql,data)
        database.commit()
    cursor.close()

def loginWithUsername(username):
    cursor = database.cursor()
    data = (username,)
    sql = """SELECT passwords.sequence FROM passwords JOIN users ON passwords.idUsername = users.id WHERE users.username = %s"""
    cursor.execute(sql,data)
    sequences = cursor.fetchall()
    cursor.close()
    return sequences

def loginWithPassword(username, password):
    cursor = database.cursor()
    data = (username,)
    sql = """SELECT passwords.password FROM passwords JOIN users ON passwords.idUsername = users.id WHERE users.username = %s"""
    cursor.execute(sql,data)
    passwords = cursor.fetchall()
    containtsPassword = True
    for passw in passwords:
        if argon2.verify(password, passw[0]):
            containtsPassword = False
    cursor.close()
    return containtsPassword
