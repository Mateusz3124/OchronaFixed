from flask import Flask, render_template, request, make_response, redirect, url_for
from collections import deque
import re

app = Flask(__name__)

@app.route("/")
def main():
    messager = request.args.get('message', '')
    missing = [1,5,6,12]
    return render_template("main.html",missing_letters = missing, message = messager)

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
            resp = make_response(render_template("bank.html"))
            resp.set_cookie("token", entered_password)
            return resp
    
    if request.method == 'GET':

        token = clearInput(request.cookies.get("token", ""))

        if token in "":
            return redirect(url_for('main', message='Please Enter Password'))
        
        if token != '12345678':     
            return redirect(url_for('main', message='Incorrect Password'))
        
        return render_template("bank.html")

@app.route("/password", methods=['POST'])
def changePassword():
    password = clearInput(request.form.get("password", ""))
    repeatedPassword = clearInput(request.form.get("repeatedPassword", ""))

    if password in "" or repeatedPassword in "":
        return render_template("bank.html", message="Incorrect Input must be letters, numbers or !@$%^&*[] and no spaces")
    
    if password == repeatedPassword:
        return render_template("bank.html", message="Success")
    else:
        return render_template("bank.html", message="Passwords aren't the same")


def clearInput(text):
    # implement bleach.clean or this method
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
