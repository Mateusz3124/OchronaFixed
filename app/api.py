from flask import Flask, render_template, request, make_response, redirect, url_for
import mysql.connector
import re

class Transaction():
    Title = None
    Amount = None
    Account = None
    Name = None
    Surname = None
    Adress = None

    def set(self, Title,Amount,Account,Name,Surname,Adress):
        self.Title = Title
        self.Amount = Amount
        self.Account = Account
        self.Name = Name
        self.Surname = Surname
        self.Adress = Adress


database = mysql.connector.connect(host='localhost',user='root',passwd='root',database='bank')
sql_insert_users = """
    INSERT INTO users (username, password, card, id)
    VALUES (%s, %s, %s, %s)
"""

sql_insert_transaction = """
    INSERT INTO transactions (title, amount, account, name, surname, address)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

def init_db():
    cursor = database.cursor()
    data = ('mati','12345678','378282246310005', 'ABC123456')
    cursor.execute(sql_insert_users,data)
    database.commit()
    data = ('ala','12345678','378282246310005', 'ABC123456')
    cursor.execute(sql_insert_users,data)
    database.commit()
    transaction = Transaction()
    transaction.set("Jedzenie",2122,"021333213","Mateusz","Gronek", "paiskowa")
    xd1 = get_data('ala', '12345678')
    xd2 = add_transaction(transaction)
    xd = get_transaction()
    change_password('mati','87654321')

def add_transaction(transaction):
    cursor = database.cursor()
    data = (transaction.Title, transaction.Amount, transaction.Account, transaction.Name, transaction.Surname, transaction.Adress)
    cursor.execute(sql_insert_transaction,data)
    database.commit()
    cursor.close()

def get_data(password, username):
    cursor = database.cursor()
    data = (password, username)
    sql = """SELECT card, id FROM users Where username = %s AND password = %s"""
    cursor.execute(sql, data)
    data = cursor.fetchall()
    cursor.close()
    return data

def get_transaction():
    cursor = database.cursor()
    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()
    cursor.close()
    return data

def change_password(username, password):
    cursor = database.cursor()
    data = (password, username)
    sql = """UPDATE users SET password = %s WHERE username = %s"""
    cursor.execute(sql,data)
    database.commit()
    cursor.close()

