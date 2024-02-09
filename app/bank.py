from flask import Flask, render_template, request, make_response, redirect, url_for, session
from sql import changeCurrentSequence, blake, setBalance, getBalanceFromAccount, getInfoAboutUser, getEmail, GetPasswordLink, addPasswordLink, deletePasswordLink, getPersonalData, getTransaction, changePassword, loginWithUsername, generateTenValues, loginWithPassword, sendTransactionToDatabase
from clearInput import clearInput, clearInputPassword
from sendEmail import sendEmail
from flask_wtf.csrf import CSRFProtect
import secrets
import random
import time
from email.mime.text import MIMEText

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
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

csrf = CSRFProtect(app)

@app.errorhandler(Exception)
def handle_error(error):
    return redirect(url_for('accountChoose', message=error))

@app.route("/", methods=['GET', 'POST'])
def accountChoose():
    messager = clearInput(request.args.get('message'))
    return render_template("account.html",message = messager)

@app.route("/favicon.ico")
def favicon():
    return "", 200

@app.route("/main", methods=['POST'])
def main():
    username = clearInput(request.form.get("username"))
    ifWantToChangePassword = clearInput(request.form.get("ifchange"))

    if ifWantToChangePassword == "True":
        link = addPasswordLink(request, username)
        msg = MIMEText(u'<h1>Change of password for your bank</h1>remember do not use any other device than the one from which you sent request to change password and do not click if you were not the one who sent it. LINK: </br><a href="https://localhost/givePassword?id={}">change password</a>'.format(link[0]),'html')
        email = getEmail(username)
        if email:
            sendEmail(email, msg)
        resp = make_response(redirect(url_for('accountChoose', message='Email sent, you have 10 minutes, if not received check username')))
        resp.set_cookie('passwordInformation', link[1],httponly = True, secure=True, samesite='Strict', max_age=600)
        return resp
    
    ran = random.uniform(0,0.5)
    time.sleep(2 + ran)

    sequences, currentSequence = loginWithUsername(username)

    if not sequences:
        missing = generateTenValues()
    
    elif len(sequences) != 10:
        return redirect(url_for('accountChoose', message='Issue with database'))
    
    else: 
        list = sequences[currentSequence[0]][0].split(",")
        intList = [int(x) for x in list]
        missing = intList

    return render_template("main.html",missing_letters = missing, user = username)

def authorizeSesion(request):
    if 'user' not in session or 'exp' not in session or 'ip' not in session:
        return True
    
    elif session['ip'] != request.access_route[-1]:
        return True 
    
    else:
        currentTime = time.time()
        if currentTime > session['exp']:
            session.pop('user')
            session.pop('exp')
            session.pop('ip')
            session.pop('csrf_token')
            return True
            
        return False

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('user')
    session.pop('exp')
    session.pop('ip')
    session.pop('csrf_token')
    return redirect(url_for('accountChoose'))

@app.route("/bank", methods=['GET', 'POST'])
def bank():
    if not authorizeSesion(request):
        message = clearInput(request.args.get('message'))
        card = clearInput(request.args.get('card'))
        id = clearInput(request.args.get('id'))
        return renderBank(message,card,id)
    
    if request.method == 'POST':
        ran = random.uniform(0,0.5)
        time.sleep(5 + ran)

        enteredPassword = ""
        username = clearInput(request.form.get("username"))
        continuation = True
        numberOFElementBeingChecked = 0
        counterOfEmptyElements = 0

        while continuation:
            letter = clearInputPassword(request.form.get(f'password{numberOFElementBeingChecked+1}'))
            numberOFElementBeingChecked += 1
            if len(enteredPassword) == 31:
                return redirect(url_for('accountChoose', message="Given password is over 30 letters"))
            if len(letter) == 1:
                counterOfEmptyElements = 0
                enteredPassword += letter
            elif len(letter) == 0:
                if counterOfEmptyElements == 2:
                    continuation = False
                else:
                    counterOfEmptyElements += 1
            else:
                sendEmail("testOchronaDanychPW@gmail.com", MIMEText(u'Tried to trick login system with entering too many letters in password. Ip of computer:'.format(request.access_route[-1]))) 
                return redirect(url_for('accountChoose', message="Error tried to trick system"))
            
        result = loginWithPassword(username, enteredPassword)

        if result is None:
            return redirect(url_for('accountChoose', message="Reached limit of 5 tries, go to local bank to fix this issue"))
        
        if result:     
            return redirect(url_for('accountChoose', message='Incorrect Password or Login'))
        
        else:
            currentTime = time.time()
            oneHour = 3600
            newTime = currentTime + oneHour
            ip = request.access_route[-1]
            session['exp'] = newTime
            session['user'] = username
            session['ip'] = ip
            resp = make_response(renderBank())
            changeCurrentSequence(username)
            return resp
    
    if request.method == 'GET':
        return redirect(url_for('accountChoose', message='Please Log In'))

def changeToTransaction(response):

    bankHistory = []
    for transactionSelected in response:
        transaction = Transaction()
        # on position 0 is id
        transaction.set(transactionSelected[1],transactionSelected[2],transactionSelected[3],transactionSelected[4],transactionSelected[5],transactionSelected[6],transactionSelected[7])
        bankHistory.append(transaction)
    return bankHistory

def renderBank(mess = "", card = "", id = ""):
    bankHistory = changeToTransaction(getTransaction(session['user']))
    userData = getInfoAboutUser(session['user'])

    if type(bankHistory) is str or type(userData) is str: 
        sendEmail("testOchronaDanychPW@gmail.com", MIMEText(u'Issue with database for user'.format(session['user']))) 
        return render_template("bank.html", message="PRoblem with database")
    
    if card and id:
        return render_template("bank.html", card_number=card, id_number=id, history=bankHistory, balance = userData[0].split(",")[0], account= userData[1])
    
    if mess:
        return render_template("bank.html", message=mess, history=bankHistory, balance = userData[0].split(",")[0], account= userData[1])
    
    return render_template("bank.html", message="", history=bankHistory, balance = userData[0].split(",")[0], account= userData[1])

@app.route("/addTransaction", methods=['POST'])
def addTransaction():
    if authorizeSesion(request):
        return redirect(url_for('accountChoose', message='Please Log In'))
    
    title = clearInput(request.form.get('Title'))
    amount = clearInput(request.form.get('Amount'))
    account = clearInput(request.form.get('Account'))
    name = clearInput(request.form.get('Name'))
    surname = clearInput(request.form.get('Surname'))
    address = clearInput(request.form.get('Adress'))

    if title in "" or amount in "" or account in "" or name in "" or surname in "" or address in "":
        return redirect(url_for('bank', message = "wrong input in transaction"))
    
    amount = amount.replace(',', '.')
    if "." in amount and len(amount.split('.')[1]) != 2:
        return redirect(url_for('bank', message = "wrong input in transaction"))
    
    try:
        if float(amount) <= 0:
            return redirect(url_for('bank', message = "wrong input in transaction"))     
        
    except ValueError:
        return redirect(url_for('bank', message = "wrong input in transaction"))
    
    transaction = Transaction()
    transaction.set(title,amount,session['user'],account,name,surname,address)
    userData = getInfoAboutUser(session['user'])
    targetData = getBalanceFromAccount(account)

    if type(userData) is str or type(targetData) is str:
        sendEmail("testOchronaDanychPW@gmail.com", MIMEText(u'Issue with database for user'.format(session['user']))) 
        return redirect(url_for('bank', message = "issue with database"))
    
    #better use int than float but for simplicity using float
    valueFrom = float(userData[0].split(",")[0]) - float(amount)
    valueTarget = float(targetData[0].split(",")[0]) + float(amount)

    if valueFrom < 0 :
        return redirect(url_for('bank', message = "not enough funds"))
    
    if sendTransactionToDatabase(transaction):
        return redirect(url_for('bank', message = "wrong recipient"))
    
    setBalance(userData[1],account, valueFrom, valueTarget, session['user'], targetData[1])
    return redirect(url_for('bank', message = "The transaction was succesful"))

@app.route("/personalData", methods=['GET'])
def data():
    if authorizeSesion(request):
        return redirect(url_for('accountChoose', message='Please Log In'))
    
    data = getPersonalData(session['user'])
    return renderBank("", data[0], data[1])

def checkForCorrectPassword(givenPassword, username):
    sequences, currentSequence = loginWithUsername(username)

    i = secrets.randbelow(10)
    list = sequences[i][0].split(",")
    sequence = [int(x) for x in list]
    
    counter = 0
    password = ""
    for letter in givenPassword:
        if counter not in sequence:
            password += letter
        counter += 1
    loginSuccesful = loginWithPassword(username, password)
    return loginSuccesful

def checkPasswordCorretness(username, givenPassword, repeatedPassword, oldPassword, ignore=True):
    if username in "" or givenPassword in "" or repeatedPassword in "" or oldPassword in "":
        return "Incorrect Input must be letters, numbers or !@#$%^&*()[]"
    
    if givenPassword != repeatedPassword:
        return "Passwords aren't the same"

    if len(givenPassword) > 30 or len(givenPassword) < 10:
        return "Password lenght is incorrect must be at least 10 letters and maximum of 30 letters"
    
    if ignore:
        passwordInCorrect = checkForCorrectPassword(oldPassword,username)
        if passwordInCorrect is None:
            return "Reached limit of 5 tries, go to local bank to fix this issue"
        if passwordInCorrect:     
            return "Incorrect Old Password"
        
    specialCharacters = "!@#$%^&*()[]"
    lowerCase = False
    upperCase = False
    number = False
    special = False

    for char in givenPassword:
        if char.islower():
            lowerCase = True
        if char.isupper():
            upperCase = True
        if char.isdigit():
            number = True
        if char in specialCharacters:
            special = True

    if not lowerCase or not upperCase or not number or not special:
        return "Passwords doesn't contain all necessary elements. Password need to have one lowercase letter, one uppercase letter, one number, and one of these symbols: !@#$%^&*()[]"

    return None

@app.route("/password", methods=['POST'])
def changePassw():
    if authorizeSesion(request):
        return redirect(url_for('accountChoose', message='Please Log In'))
    
    givenPassword = clearInputPassword(request.form.get("password"))
    repeatedPassword = clearInputPassword(request.form.get("repeatedPassword"))
    oldPassword = clearInputPassword(request.form.get("oldPassword"))

    passwordIncorrect = checkPasswordCorretness(session['user'], givenPassword, repeatedPassword, oldPassword)

    if passwordIncorrect is not None and passwordIncorrect in "Reached limit of 5 tries, go to local bank to fix this issue":
        return logout()
    
    if passwordIncorrect is not None:
        return renderBank(passwordIncorrect)
    
    changePassword(session['user'], givenPassword)
    session.pop('user')
    session.pop('exp')
    session.pop('csrf_token')
    session.pop('ip')
    return redirect(url_for('accountChoose', message='Changed password'))

@app.route("/givePassword", methods=['GET','POST'])
def givePassword():
    if request.method == "GET":
        return render_template("changePassword.html", message="")
    
    cookieSecret = request.cookies.get('passwordInformation').split(":")
    cookieHash = clearInput(cookieSecret[0])
    ip = clearInput(cookieSecret[1])
    id = clearInput(request.form.get('id'))

    if id in "" or cookieHash in "" or ip in "" or len(id) > 15:
        return redirect(url_for('accountChoose', message='Issue with given link, maybe reached limit of 10 minutes'))
    
    if request.access_route[-1] != ip:
        return redirect(url_for('accountChoose', message='Please repeat but do not change internet connection'))
    
    username = clearInput(request.form.get("username")) 

    if cookieHash != blake(username, str(request.access_route[-1])):
        return redirect(url_for('accountChoose', message='Please repeat but do not change internet connection'))
    
    links = GetPasswordLink()
    isCookieHashInCorrect = True
    for link in links:
        if id in link[0] and cookieHash in link[1].split(":")[0]:
            isCookieHashInCorrect = False

    if isCookieHashInCorrect:
        return redirect(url_for('accountChoose', message='Issue with given link'))
       
    givenPassword = clearInputPassword(request.form.get("password"))
    repeatedPassword = clearInputPassword(request.form.get("repeatedPassword"))
    variable = checkPasswordCorretness(username, givenPassword, repeatedPassword, "w", False)

    if variable is not None:
        return render_template("changePassword.html", message=variable)
    
    if variable is not None and variable in "Reached limit of 5 tries, go to local bank to fix this issue":
        return render_template("changePassword.html", message="Reached limit of 5 tries, go to local bank to fix this issue")
    
    changePassword(username, givenPassword)
    deletePasswordLink(id)
    
    return redirect(url_for('accountChoose', message='Changed password'))   
    
    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000, threads=4)
