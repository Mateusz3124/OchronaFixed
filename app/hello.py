from flask import Flask, render_template, request, make_response, redirect, url_for
from api import init_db, add_transaction, change_password
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

init_db()

@app.route("/")
def main():
    messager = request.args.get('message', '')
    missing = [1,5,6,12]
    return render_template("main.html",missing_letters = missing, message = messager)

def authorizeToken(request):
    token = clearInput(request.cookies.get("token", ""))

    if token in "":
        return redirect(url_for('main', message='Please Enter Password'))
    
    if token != '12345678':     
        return redirect(url_for('main', message='Incorrect Password'))

@app.route("/bank", methods=['GET', 'POST'])
def bank():
    if request.method == 'POST':
        entered_password = ""
        username = clearInput(request.form.get("username"))
        continuation = True
        i = 0
        counter = 0
        while continuation:
            letter = clearInput(request.form.get(f'password{i+1}', ''))
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
                return redirect(url_for('main', message="Error tried to trick system and add password with too many letters"))
        
        if entered_password != '12345678' or username != 'mati':     
            return redirect(url_for('main', message='Incorrect Password or Login'))
        else:
            resp = make_response(renderBank())
            resp.set_cookie("token", entered_password)
            return resp
    
    if request.method == 'GET':
        authorizeToken(request)
        renderBank()

def renderBank(mess = "", card = "", id = ""):
    bankHistory = []
    transaction = Transaction()
    transaction.set("Jedzenie",2122,"021333213","Mateusz","Gronek", "paiskowa")
    bankHistory.append(transaction)
    transaction.set("Jedzenie",11133221,"3123213","Mielarek","Mog", "piaskowa")
    bankHistory.append(transaction)
    if card and id:
        return render_template("bank.html", card_number=card, id_number=id, history=bankHistory)
    if mess:
        return render_template("bank.html", message=mess, history=bankHistory)
    return render_template("bank.html", history=bankHistory)

@app.route("/personalData", methods=['GET'])
def data():
    authorizeToken(request)
    return renderBank("", 2321321, 222118)

@app.route("/password", methods=['POST'])
def changePassword():
    authorizeToken(request)
    password = clearInput(request.form.get("password", ""))
    repeatedPassword = clearInput(request.form.get("repeatedPassword", ""))

    if password in "" or repeatedPassword in "":
        return renderBank("Incorrect Input must be letters, numbers or !@$%^&*[] and no spaces")
    
    if password == repeatedPassword:
        return renderBank("Success")
    else:
        return renderBank("Passwords aren't the same")


def clearInput(text):
    pattern = re.compile(r'^[a-zA-Z0-9!@$%^&*\[\]]+$')
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
