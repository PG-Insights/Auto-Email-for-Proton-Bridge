import os
import time
import sys
import smtplib
import base64
from pathlib import Path
from dotenv import load_dotenv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
if str(Path(__file__).parents[0]) not in sys.path:
    sys.path.append(str(Path(__file__).parents[0]))
    sys.path.append(str(Path(__file__).parents[1]))
from get_files import GetFiles

load_dotenv()


class ComposeEmail:
    
    _vm_email_path = Path('/', 'home', 'opc', 'email_venv')
    _ip = '127.0.0.1'
    _port = 1025
    
    def __init__(
            self,
            emails_list_path: str,
            html_path: str,
            from_email: str='contact@cupsnbowls.com',
            *,
            png_path=None,
            pdf_path=None):
        self.msg = MIMEMultipart()
        self.from_email = from_email
        self.emails_list_path = emails_list_path
        self.emails_list = GetFiles(self.emails_list_path).data
        self.html_obj = GetFiles(html_path)
        self.email_subject = self.html_obj.filename
        if png_path:
            self.png_path = Path(png_path)
        else:
            self.png_path = None
        
        if pdf_path:
            self.pdf_path = Path(pdf_path)
        else:
            self.pdf_path = None
        
        self.composed_email = self.compose_html_email()
        
    def compose_html_email(self) -> MIMEText:   
        self.msg['From'] = self.from_email
        self.msg['To'] = self.from_email
        self.msg['Subject'] = self.email_subject
        self._add_html_to_msg()
        if self.png_path:
            self.add_png_to_email()
        if self.pdf_path:
            self.add_pdf_to_email()
        return self.msg.as_string()
    
    def _add_html_to_msg(self):
        try:
            html = GetFiles.decode_html_str(self.html_obj.data)
            mime_html = MIMEText(html, 'html')
            self.msg.attach(mime_html)
        except base64.binascii.Error:
            pass
        except UnicodeDecodeError:
            pass
        
    def add_png_to_email(self):
        img_html = MIMEText('<img src="cid:image1">', 'html')
        self.msg.attach(img_html)
        image = MIMEImage(GetFiles(self.png_path).data)
        image.add_header('Content-ID', '<image1>')
        self.msg.attach(image)
        
    def get_pdf_for_email(self) -> bytes:
        try:
            pdf_obj = GetFiles(self.pdf_path)
            payload = MIMEBase(
                'application', 
                'octate-stream', 
                Name=f'{pdf_obj.filename}.pdf',
            )
            payload.set_payload(pdf_obj.data)
            encoders.encode_base64(payload)
            payload.add_header(
                'Content-Decomposition', 
                'attachment', 
                filename=f'{pdf_obj.filename}.pdf',
            )
            return payload
        except Exception as e:
            print('\nError:', e, '\n')
            return None
        
    def add_pdf_to_email(self):
        pdf_payload = self.get_pdf_for_email()
        self.msg.attach(pdf_payload)
    
    def get_unique_emails_from_series_or_list(self) -> list:
        if isinstance(self.emails_list, list):
            no_dups = set(self.emails_list)
            no_dups_list = list(no_dups)
        else:
            no_dups = self.emails_list['emails'].unique()
            no_dups_list = no_dups.tolist()
        return no_dups_list
    
    def send_email_func(self) -> None:  
        emails_list = self.get_unique_emails_from_series_or_list()
        with smtplib.SMTP(self._ip, self._port) as smtp:
            smtp.starttls()
            smtp.login(os.environ.get('UNAME'), os.environ.get('PASS'))
            time.sleep(.1)
            smtp.sendmail(
                self.from_email, 
                [self.from_email] + emails_list, 
                self.email_message
            )
            smtp.quit()
        print('\nThe email(s) have been sent\n')


if __name__ == '__main__':    
    app_dir = Path(__file__).parents[1]
    html_path = None #f'{app_dir}/html_files/Cups and Bowls Newsletter 1.html' 
    emails_path = None #f'{app_dir}/email_lists/test_list_1.csv'  
    png_path = None #f'{app_dir}/email_png/no_chalk_pdf_png_test.png'
    pdf_path = None #f'{app_dir}/pdf_attach/cnb_newsletter_1.pdf' 
    if emails_path == None or html_path == None:
        import argparse
        parser = argparse.ArgumentParser(
            description='Send email with html content'
        )
        parser.add_argument(
            'html_path', 
            type=str, 
            help='HTML File Path'
        )
        parser.add_argument(
            'emails_path', 
            type=str, 
            help='Path to CSV or Excel with "emails" column'
        )
        
        parser.add_argument(
            '--png_path',
            type=str, 
            default=None, 
            help='Path to PNG for email body'
        )
        parser.add_argument(
            '--pdf_path', 
            type=str, 
            default=None, 
            help='PDF File Path'
        )
        
        args = parser.parse_args()

        emails_path = args.emails_path
        html_path = args.html_path
        png_path = args.png_path if args.png_path else None
        pdf_path = args.pdf_path if args.pdf_path else None
    
    # Create the email_obj from either args or data from IDE
    email_obj = ComposeEmail(
        emails_path,
        html_path,
        png_path=png_path,
        pdf_path=pdf_path
    )

    try:
        email_obj.send_email_func()
    except ConnectionRefusedError:
        print(
            """
            
**********************************************
    Your email server is not running!
**********************************************
            
            """
        )
        
