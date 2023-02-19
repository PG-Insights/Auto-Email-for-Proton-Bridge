#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
You must already have an instance of the email_server running on the
same machine, as well as the Proton-Bridge mail client

Created on Sun Feb 19 09:26:48 2023

@author: dale
"""

import sys
from pathlib import Path

MAIN_DIR = Path(__file__).parent

if str(MAIN_DIR) not in sys.path:
    sys.path.append(str(MAIN_DIR))
if str(Path(MAIN_DIR, '__helpers__')) not in sys.path:
    sys.path.append(str(Path(MAIN_DIR, '__helpers__')))

import compose_email
from email_helpers import GetFiles
from ssh_login import ssh_login_and_run_function
    

def login_and_send_data(html_path, csv_or_excel_path):
    html_file = GetFiles(html_path)
    email_values = GetFiles(csv_or_excel_path)
    ssh_login_and_run_function(
        compose_email.send_email_func(
            subject=html_file.filename, 
            list_of_emails=email_values.data['emails'], 
            txt=None,
            html=html_file.data)
    )
    
    
if __name__ == '__main__':
    html_path = None  # Change this to html path if running in an IDE
    csv_or_excel_path = None # Change this if running from IDE
    if html_path is None or csv_or_excel_path is None:
        import argparse
        parser = argparse.ArgumentParser(
            description='Send email with html content'
            )
        parser.add_argument(
            'html_path', 
            type=str, 
            help='Path to the HTML file'
            )
        parser.add_argument(
            'csv_or_excel_path', 
            type=str, 
            help='Path to the csv or excel file with email addresses'
            )
        args = parser.parse_args()
        login_and_send_data(args.html_path, args.csv_or_excel_path)
    else:
        login_and_send_data(html_path, csv_or_excel_path)
        
        
        
    