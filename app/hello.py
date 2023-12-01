from flask import Flask, render_template, request, make_response, redirect, url_for
import markdown
from collections import deque

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
    print 
    if password == repeatedPassword:
        return render_template("bank.html", message="Success")
    else:
        return render_template("bank.html", message="Passwords aren't the same")


def clearInput(text):
    # implement bleach.clean
    return text

@app.route("/render", methods=['POST'])
def render():
    md = request.form.get("markdown","")
    rendered = markdown.markdown(md)
    notes.append(rendered)
    return render_template("markdown.html", rendered=rendered)

@app.route("/render/<rendered_id>")
def render_old(rendered_id):
    if int(rendered_id) > len(notes):
        return "Wrong note id", 404

    rendered = notes[int(rendered_id) - 1]
    return render_template("markdown.html", rendered=rendered)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)