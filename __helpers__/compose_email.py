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
        self.emails_list_path = Path(emails_list_path)
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
    
    @staticmethod
    def get_unique_emails_from_series_or_list(series_or_list) -> list:
        if isinstance(series_or_list, list):
            no_dups = set(series_or_list)
            no_dups_list = list(no_dups)
        else:
            no_dups = series_or_list.unique()
            no_dups_list = no_dups.tolist()
        return no_dups_list
    
    def send_email_func(self) -> None:  
        emails_list = self.get_unique_emails_from_series_or_list(
            self.emails_list
        )
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
    emails_path = f'{app_dir}/email_lists/test_list_1.csv'  
    html_path = f'{app_dir}/html_files/Cups and Bowls Newsletter 1.html' 
    png_path = f'{app_dir}/email_png/no_chalk_pdf_png_test.png'
    pdf_path = f'{app_dir}/pdf_attach/cnb_newsletter_1.pdf' 
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
            'png_path', 
            type=str, 
            help='Path to PNG for email body'
        )
        parser.add_argument(
            'pdf_path', 
            type=str, 
            help='PDF File Path'
        )
        args = parser.parse_args()
        html_file = GetFiles(args.html_file)
        subject = html_file.filename
        emails_path = GetFiles(args.emails_csv_or_excel).data['emails']
        html_path = html_file.data
        png_path = args.png_path
        pdf_path = args.pdf_file
    # Create the email_obj from either args or data from IDE
    email_obj = ComposeEmail(
        emails_path,
        html_path,
        png_path=png_path,
        pdf_path=pdf_path
    )
    print(email_obj.composed_email)

        
