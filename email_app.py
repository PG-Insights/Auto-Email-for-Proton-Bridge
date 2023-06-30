#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
You must already have an instance of the email_server running on the
remote machine, as well as the Proton-Bridge mail client

Created on Sun Feb 19 09:26:48 2023

@author: dale
"""

import sys
from pathlib import Path
from smtplib import SMTPDataError

MAIN_DIR = Path(__file__).parent

if str(MAIN_DIR) not in sys.path:
    sys.path.append(str(MAIN_DIR))
if str(Path(MAIN_DIR, '__helpers__')) not in sys.path:
    sys.path.append(str(Path(MAIN_DIR, '__helpers__')))


if __name__ == '__main__':
    import time
    import commands_for_remote_email as commands
    from ssh_login import return_ssh_connection
    
    app_dir = Path(__file__).parents[1]
    html_path = None #f'{app_dir}/html_files/Cups and Bowls Newsletter 1.html'
    from_email = None #'contact@cupsnbowls.com'
    url_str = None #'https://cupsnbowls.com/email_monitoring/email_test_1'
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
            'from_email', 
            type=str, 
            help='Email address sending emails from'
        )
        parser.add_argument(
            '--url_str', 
            type=str,
            default=None,
            help='Final URL path for tracking'
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
        from_email = args.from_email
        url_str = args.url_str if args.url_str else None
        png_path = args.png_path if args.png_path else None
        pdf_path = args.pdf_path if args.pdf_path else None

        conn = return_ssh_connection()
        time.sleep(.5)
        try:
            commands.transfer_file_to_remote(
                conn,
                args.html_path,
                '/home/opc/email_venv/html_files',
            )
        except:
            commands.transfer_large_file_to_remote(
                conn,
                args.html_path,
                '/home/opc/email_venv/html_files',
            )
        time.sleep(.5)
        commands.transfer_file_to_remote(
            conn,
            args.emails_path,
            '/home/opc/email_venv/email_lists',
        )
        time.sleep(.5)
        if png_path:
            commands.transfer_file_to_remote(
                conn,
                args.png_path,
                '/home/opc/email_venv/email_png',
            )
            time.sleep(.5)
        if pdf_path:
            commands.transfer_file_to_remote(
                conn,
                args.pdf_path,
                '/home/opc/email_venv/pdf_attach',
            )
            time.sleep(.5)

        c1, c2, c3 = commands.create_send_email_commands(
            args.html_path,
            args.emails_path,
            url_str=args.url_str,
            png_path=args.png_path,
            pdf_path=args.pdf_path,
        )        
        time.sleep(.5)
        commands.run_remote_command_in_shell(conn, c1)
        time.sleep(.5)
        commands.run_remote_command_in_shell(conn, c2)
        time.sleep(.5)
        commands.run_remote_command_in_shell(conn, c3)
        print('\nThe files have been successfully removed\n')
