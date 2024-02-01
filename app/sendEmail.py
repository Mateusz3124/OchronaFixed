import smtplib, ssl

def sendEmail(email, msg):
    smtp_server = "smtp.gmail.com"
    port = 587 
    #email from which you want to send mails
    sender_email = ""
    password = ""

    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context)
        server.login(sender_email, password)
        msg['Subject'] = 'Notification from bank'
        msg['From'] = 'xxx'
        msg['To'] = 'xxx'
        if email:
            server.sendmail(sender_email, email, msg.as_string())
            return
        else:
            return
    except Exception as e:
        print(e)
    finally:
        server.quit() 