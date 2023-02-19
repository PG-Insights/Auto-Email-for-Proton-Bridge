import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()


def compose_html_email(subject, from_email,  txt=None, html=None) -> MIMEText:
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = from_email
    msg['Subject'] = str(subject)
    if txt:
        mime_text = MIMEText(txt, 'plain')
        msg.attach(mime_text)
    if html:
        mime_html = MIMEText(html, 'html')
        msg.attach(mime_html)
    message_str = msg.as_string()
    return message_str


def get_unique_emails_from_series_or_list(series_or_list) -> list:
    if isinstance(series_or_list, list):
        no_dups = set(series_or_list)
        no_dups_list = list(no_dups)
    else:
        no_dups = series_or_list.unique()
        no_dups_list = no_dups.tolist()
    return no_dups_list


def send_email_func(subject,
                    list_of_emails,
                    from_email='letmoplay@letmoplay.com',
                    txt=None,
                    html=None) -> None:
    email_message = compose_html_email(
        subject, from_email,  txt=txt, html=html)
    emails_list = get_unique_emails_from_series_or_list(list_of_emails)
    with smtplib.SMTP('127.0.0.1', 1025) as smtp:
        smtp.starttls()
        smtp.login(os.environ.get('UNAME'), os.environ.get('PASS'))
        time.sleep(.1)
        smtp.sendmail(from_email, [from_email] + emails_list, email_message)
        smtp.quit()
    print('\nThe email(s) have been sent\n')


if __name__ == '__main__':
    import time
    test_emails_list = ['dludwins@outlook.com', 'dludwins0809@gmail.com']
    send_email_func('Test Email', test_emails_list, txt='Text Line',
                    html='<h1>HTML LINE</h1><br><h3 style="color:red";>SMALLER RED HTML</h3>')
