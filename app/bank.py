from flask import Flask, render_template, request, make_response, redirect, url_for, session
from api import getData, getTransaction, changePassword, loginWithUsername, generateTenValues, loginWithPassword, sendTransactionToDatabase
from flask_wtf.csrf import CSRFProtect, CSRFError
import random
import time
import re

class Transaction():
    Title = None
    Amount = None
    FromAccount = None
    Account = None
    Name = None
    Surname = None
    Adress = None

    def set(self, Title,Amount,FromAccount,Account,Name,Surname,Adress):
        self.Title = Title
        self.Amount = Amount
        self.FromAccount = FromAccount
        self.Account = Account
        self.Name = Name
        self.Surname = Surname
        self.Adress = Adress


app = Flask(__name__)
app.config['SECRET_KEY'] = '123c1nrjcn1ictrfwyaid7tc32rcimy87crgts87emgyi32cry89r43y872ym9831yrv87t1guv9mv7842ym7v5t4m198ymv5t27ym45b747mbt5427y62m895tcgv8m924598ytv752uvtm25t7952ym9mtg578b2578yv2tm78g'
csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return redirect(url_for('accountChoose', message='Something went wrong try logging again'))

@app.route("/", methods=['GET', 'POST'])
def accountChoose():
    messager = clearInput(request.args.get('message'))
    return render_template("account.html",message = messager)

@app.route("/main", methods=['POST'])
def main():
    time.sleep(2)
    username = clearInput(request.form.get("username"))
    sequences = loginWithUsername(username)
    if not sequences:
        missing = generateTenValues()
    elif len(sequences) != 10:
        return redirect(url_for('accountChoose', message='Issue with database'))
    else: 
        random.seed(time.perf_counter())
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

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('user')
    return redirect(url_for('accountChoose'))

@app.route("/bank", methods=['GET', 'POST'])
def bank():
    if not authorizeSesion(request):
        message = clearInput(request.args.get('message'))
        card = clearInput(request.args.get('card'))
        id = clearInput(request.args.get('id'))
        return renderBank(message,card,id)
    
    if request.method == 'POST':
        time.sleep(5)
        entered_password = ""
        username = clearInput(request.form.get("username"))
        continuation = True
        i = 0
        counter = 0
        while continuation:
            letter = clearInput(request.form.get(f'password{i+1}'))
            i += 1
            if len(entered_password) == 30:
                return redirect(url_for('accountChoose', message="Given password is over 30 letters"))
            if len(letter) == 1:
                counter = 0
                entered_password += letter
            elif len(letter) == 0:
                if counter == 2:
                    continuation = False
                else:
                    counter += 1
            else:    
                return redirect(url_for('accountChoose', message="Error tried to trick system"))
        result = loginWithPassword(username, entered_password)
        if result is None:
            return redirect(url_for('accountChoose', message="Reached limit of 5 tries, go to local bank to fix this issue"))
        if result:     
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
        # on position 0 id
        transaction.set(item[1],item[2],item[3],item[4],item[5],item[6],item[7])
        bankHistory.append(transaction)
    return bankHistory

def renderBank(mess = "", card = "", id = ""):
    bankHistory = changeToTransaction(getTransaction(session['user']))
    if card and id:
        return render_template("bank.html", card_number=card, id_number=id, history=bankHistory)
    if mess:
        return render_template("bank.html", message=mess, history=bankHistory)
    return render_template("bank.html", message="", history=bankHistory)

@app.route("/addTransaction", methods=['POST'])
def addTransaction():
    if authorizeSesion(request):
        return redirect(url_for('accountChoose', message='Please Log In'))
    title = clearInput(request.form['Title'])
    amount = clearInput(request.form['Amount'])
    account = clearInput(request.form['Account'])
    name = clearInput(request.form['Name'])
    surname = clearInput(request.form['Surname'])
    address = clearInput(request.form['Adress'])
    if title in "" or amount in "" or account in "" or name in "" or surname in "" or address in "":
        return redirect(url_for('bank', message = "wrong input in transaction"))
    transaction = Transaction()
    transaction.set(title,amount,session['user'],account,name,surname,address)
    if sendTransactionToDatabase(transaction):
        return redirect(url_for('bank', message = "wrong recipient"))
    return redirect(url_for('bank', message = "The transaction was succesful"))




@app.route("/personalData", methods=['GET'])
def data():
    if authorizeSesion(request):
        return redirect(url_for('accountChoose', message='Please Log In'))
    data = getData(session['user'])
    return renderBank("", data[0], data[1])

def checkForCorrectPassword(givenPassword):
    sequences = loginWithUsername(session['user'])

    random.seed(time.perf_counter())
    i = random.randint(0, 7)
    list = sequences[i][0].split(",")
    sequence = [int(x) for x in list]
    
    counter = 0
    password = ""
    for letter in givenPassword:
        if counter not in sequence:
            password += letter
        counter += 1
    checker = loginWithPassword(session['user'], password)
    return checker

@app.route("/password", methods=['POST'])
def changePassw():
    if authorizeSesion(request):
        return redirect(url_for('accountChoose', message='Please Log In'))
    
    givenPassword = clearInput(request.form.get("password"))
    repeatedPassword = clearInput(request.form.get("repeatedPassword"))
    oldPassword = clearInput(request.form.get("oldPassword"))

    if givenPassword in "" or repeatedPassword in "" or oldPassword in "":
        return renderBank("Incorrect Input must be letters, numbers or !@$%^&*[]")
    
    if givenPassword != repeatedPassword:
        return renderBank("Passwords aren't the same")

    if len(givenPassword) > 30 or len(givenPassword) < 10:
        return renderBank("Password lenght is incorrect must be at least 10 letters and maximum of 30 letters")

    checker = checkForCorrectPassword(oldPassword)
    if checker is None:
        return renderBank("Reached limit of 5 tries, go to local bank to fix this issue")
    if checker:     
        return renderBank('Incorrect Password')
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
    return redirect(url_for('bank', message = "Success, password changed"))
        
def clearInput(text):
    pattern = re.compile(r'^[., a-zA-Z0-9!@$%^&*\[\]]+$')
    if text is None:
        return ""
    if len(text) > 60:
        return ""
    match = pattern.match(text)
    if bool(match):
        return text
    else:
        return ""
    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000, threads=4)
