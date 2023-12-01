from flask import Flask, render_template, request, make_response, redirect, url_for
from collections import deque
import re

app = Flask(__name__)

class CustomError(Exception):
    def __init__(self, message):
        super().__init__(message)

notes = []
recent_users = deque(maxlen=3)
PASSWORD_LENGTH = 8

@app.route("/")
def main():
    messager = request.args.get('message', '')
    return render_template("main.html", password_length=PASSWORD_LENGTH, message = messager)


@app.route("/bank", methods=['GET', 'POST'])
def bank():
    username = "Mateusz"
    entered_password = ""
    if request.method == 'POST':

        for i in range(PASSWORD_LENGTH):
            letter = request.form.get(f'password{i+1}', '')
            if len(letter) != 1:    
                return redirect(url_for('main', message="Error tried to add password with too many letters"))
            entered_password += letter
        

        if entered_password != '12345678':     
            return redirect(url_for('main', message='Incorrect Password'))
        
        else:
            resp = make_response(render_template("bank.html"))
            resp.set_cookie("password", entered_password)
            return resp
    
    if request.method == 'GET':

        password = request.cookies.get("password")

        if password is None:
            return redirect(url_for('main', message='Please Enter Password'))
        
        if password != '12345678':     
            return redirect(url_for('main', message='Incorrect Password'))
        
        return render_template("bank.html")

@app.route("/password", methods=['POST'])
def changePassword():
    password = clearInput(request.form.get("password"))
    repeatedPassword = clearInput(request.form.get("repeatedPassword"))

    if password in "" or repeatedPassword in "":
        return render_template("bank.html", message="Incorrect Input must be letters, numbers or !@#$%^&*")
    
    if password == repeatedPassword:
        return render_template("bank.html", message="Success")
    else:
        return render_template("bank.html", message="Passwords aren't the same")


def clearInput(text):
    # implement bleach.clean or this method
    pattern = re.compile(r'^[a-zA-Z0-9!@#$%^&*]+$')
    match = pattern.match(text)
    if bool(match):
        return text
    else:
        return ""
    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
