import smtplib, ssl

def sendEmail(email, msg):
    smtp_server = "smtp.gmail.com"
    port = 587 
    sender_email = "testOchronaDanychPW@gmail.com"
    password = "lvfwzupsxywsmgws"

    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
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
        #implement here
        print(e)
    finally:
        server.quit() 