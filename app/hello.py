import math
from flask import Flask, render_template, request, make_response, redirect, url_for, session
from api import getTransaction, changePassword, loginWithUsername, generateTenValues, loginWithPassword
from flask_wtf.csrf import CSRFProtect, CSRFError
import datetime
import random
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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return redirect(url_for('accountChoose', message='Something went wrong try logging again'))

@app.route("/")
def accountChoose():
    messager = clearInput(request.args.get('message'))
    return render_template("account.html",message = messager)


@app.route("/main", methods=['POST'])
def main():
    username = clearInput(request.form.get("username"))
    sequences = loginWithUsername(username)
    if not sequences:
        missing = generateTenValues()
    else: 
        i = random.randint(0, 7)
        list = sequences[i][0].split(",")
        intList = [int(x) for x in list]
        missing = intList
    return render_template("main.html",missing_letters = missing, user = username)

def authorizeSesion(request):
    if 'user' not in session:
        return True
    else:
        return False

@app.route("/bank", methods=['GET', 'POST'])
def bank():
    if request.method == 'POST':
        entered_password = ""
        username = clearInput(request.form.get("username"))
        continuation = True
        i = 0
        counter = 0
        while continuation:
            letter = clearInput(request.form.get(f'password{i+1}'))
            i += 1
            if len(letter) == 1:
                counter = 0
                entered_password += letter
            elif len(letter) == 0:
                if counter == 2:
                    continuation = False
                else:
                    counter += 1
            else:    
                return redirect(url_for('accountChoose', message="Error tried to trick system and add password with too many letters in one square"))
        
        if loginWithPassword(username, entered_password):     
            return redirect(url_for('accountChoose', message='Incorrect Password or Login'))
        else:
            session['user'] = username
            resp = make_response(renderBank())
            return resp
    
    if request.method == 'GET':
        if authorizeSesion(request):
            return redirect(url_for('accountChoose', message='Please Log In'))
        return renderBank()

def changeToTransaction(response):
    bankHistory = []
    for item in response:
        transaction = Transaction()
        transaction.set(item[0],item[1],item[2],item[3],item[4],item[5])
        bankHistory.append(transaction)
    return bankHistory

def renderBank(mess = "", card = "", id = ""):
    bankHistory = changeToTransaction(getTransaction(session['user']))
    if card and id:
        return render_template("bank.html", card_number=card, id_number=id, history=bankHistory)
    if mess:
        return render_template("bank.html", message=mess, history=bankHistory)
    return render_template("bank.html", message="", history=bankHistory)

@app.route("/personalData", methods=['GET'])
def data():
    if authorizeSesion(request):
        return redirect(url_for('main', message='Please Log In'))
    
    return renderBank("", 2321321, 222118)

@app.route("/password", methods=['POST'])
def changePassw():
    if authorizeSesion(request):
        return redirect(url_for('main', message='Please Log In'))
    
    givenPassword = clearInput(request.form.get("password"))
    repeatedPassword = clearInput(request.form.get("repeatedPassword"))

    if givenPassword in "" or repeatedPassword in "":
        return renderBank("Incorrect Input must be letters, numbers or !@$%^&*[] and no spaces")
    
    if givenPassword != repeatedPassword:
        return renderBank("Passwords aren't the same")

    if len(givenPassword) > 30 or len(givenPassword) < 10:
        return renderBank("Password lenght is incorrect must be at least 10 letters and maximum of 30 letters")

    specialCharacters = "!@$%^&*[]"
    lowerCase = True
    upperCase = True
    number = True
    special = True

    for char in givenPassword:
        if char.islower():
            lowerCase = False
        if char.isupper():
            upperCase = False
        if char.isdigit():
            number = False
        if char in specialCharacters:
            special = False

    if lowerCase or upperCase or number or special:
        return renderBank("Passwords doesn't contain all necessary elements. Password need to have one lowercase letter, one uppercase letter, one number, and one of these symbols: !@$%^&*[]")

    changePassword(session['user'], givenPassword)
    return renderBank("Success, password changed")
        
def clearInput(text):
    pattern = re.compile(r'^[ a-zA-Z0-9!@$%^&*\[\]]+$')
    if text is None:
        return ""
    match = pattern.match(text)
    if bool(match):
        return text
    else:
        return ""
    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
