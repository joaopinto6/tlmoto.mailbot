from flask import Flask, request
from email.message import EmailMessage
import ssl
import smtplib
from decouple import config

app = Flask(__name__)

@app.route('/')
def route():
    return 'Working...'

@app.route('/sendmail', methods=['POST'])
def send_email():
    email_sender = config('EMAIL_SENDER')
    email_password = config('EMAIL_PASSWORD')
    email_receiver = config('EMAIL_RECEIVER')

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    subject = f"New message from {name} - {email}"
    body = message

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    
    return '', 204

if __name__ == '__main__':
    app.run()
