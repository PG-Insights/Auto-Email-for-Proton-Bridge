import os
import time
import sys
import smtplib
from pathlib import Path
from dotenv import load_dotenv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
if str(Path(__file__).parents[0]) not in sys.path:
    sys.path.append(str(Path(__file__).parents[0]))
    sys.path.append(str(Path(__file__).parents[1]))

load_dotenv()


def compose_html_email(subject, from_email,  html=None, pdf=None) -> MIMEText:   
    from email_helpers import GetFiles
    import base64
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = from_email
    msg['Subject'] = str(subject)
    try:
        html = GetFiles.decode_html_str(html)
    except base64.binascii.Error:
        pass
    except UnicodeDecodeError:
        pass
    pdf_payload = get_pdf_for_email(pdf)
    if pdf_payload != None:
        msg.attach(pdf_payload)
    mime_html = MIMEText(html, 'html')
    msg.attach(mime_html)
    message_str = msg.as_string()
    return message_str


def get_pdf_for_email(pdf: str) -> bytes:
    try:
        pdfname = GetFiles.return_only_file_name(pdf)
        binary_pdf = GetFiles(pdf)
        payload = MIMEBase('application', 'octate-stream', Name=pdfname)
        payload.set_payload((binary_pdf).read())
        encoders.encode_base64(payload)
        payload.add_header(
            'Content-Decomposition', 
            'attachment', 
            filename=pdfname
        )
        return payload
    except Exception as e:
        print(e)
        return None


def get_unique_emails_from_series_or_list(series_or_list) -> list:
    if isinstance(series_or_list, list):
        no_dups = set(series_or_list)
        no_dups_list = list(no_dups)
    else:
        no_dups = series_or_list.unique()
        no_dups_list = no_dups.tolist()
    return no_dups_list


def send_email_func(subject='Let MO Play!',
                    list_of_emails=None,
                    from_email='pginsights@pginsights.org',
                    html=None,
                    pdf=None) -> None:
    email_message = compose_html_email(subject, from_email, html=html, pdf=pdf)
    emails_list = get_unique_emails_from_series_or_list(list_of_emails)
    with smtplib.SMTP('127.0.0.1', 1025) as smtp:
        smtp.starttls()
        smtp.login(os.environ.get('UNAME'), os.environ.get('PASS'))
        time.sleep(.1)
        smtp.sendmail(from_email, [from_email] + emails_list, email_message)
        smtp.quit()
    print('\nThe email(s) have been sent\n')


if __name__ == '__main__':
    from email_helpers import GetFiles
    
    subject = None  #'Test'
    emails_list = None  #['dludwins@outlook.com']
    html_str = None  #'<html><h1>test</h1></html>'
    pdf_attach = None  # /path/to/file.pdf
    if html_str == None or emails_list == None or subject == None:
        import argparse
        parser = argparse.ArgumentParser(
            description='Send email with html content'
            )
        parser.add_argument(
            'html_file', 
            type=str, 
            help='HTML File Path'
            )
        parser.add_argument(
            'emails_csv_or_excel', 
            type=str, 
            help='Path to CSV or Excel with Emails column'
            )
        parser.add_argument(
            'pdf_file', 
            type=str, 
            help='PDF File Path'
            )
        args = parser.parse_args()
        html_file = GetFiles(args.html_file)
        subject = html_file.filename
        emails_list = GetFiles(args.emails_csv_or_excel).data['emails']
        html_str = html_file.data
        pdf_attach = args.pdf_file
    # Run the send_email_func with either args or data from IDE
    send_email_func(
        subject=subject, 
        list_of_emails=emails_list, 
        html=html_str,
        pdf=pdf_attach,
        )
        
