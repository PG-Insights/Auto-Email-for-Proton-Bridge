import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

def get_test_email():
    msg = MIMEText('This is a test')
    msg['From'] = 'pginsights@pginsights.org'
    msg['To'] = 'dludwins@outlook.com'
    msg['Subject'] = 'EMAIL TEST'
    return msg

if __name__ == '__main__':
    import time
    with smtplib.SMTP('127.0.0.1', 1025) as smtp:
        smtp.starttls()
        smtp.login(os.environ.get('UNAME'), os.environ.get('PASS'))
        time.sleep(.1)
        smtp.send_message(get_test_email())
    print('\nThe test in complete\n') 

