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


if __name__ == '__main__':
    import time
    import commands_for_remote_email as commands
    from ssh_login import return_ssh_connection
    
    html_path = None  # Change this to html path if running in an IDE
    csv_or_excel_path = None  # Change this if running from IDE
    pdf_attach = None  # Change this to PDF path if needed
    if html_path is None or csv_or_excel_path is None:
        import argparse
        parser = argparse.ArgumentParser(
            description='Send email with html content on remote machine'
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
        parser.add_argument(
            'png_path', 
            type=str, 
            help='Path to PNG for email body'
            )
        parser.add_argument(
            'pdf_path',
            type=str,
            help='Path to the PDF to include as attachment'
        )
        args = parser.parse_args()

        conn = return_ssh_connection()
        time.sleep(.5)
        commands.trasfer_file_to_remote(
            conn,
            args.html_path,
            '/home/opc/email_venv/html_files',
        )
        time.sleep(.5)
        commands.trasfer_file_to_remote(
            conn,
            args.csv_or_excel_path,
            '/home/opc/email_venv/email_lists',
        )
        time.sleep(.5)
        commands.trasfer_file_to_remote(
            conn,
            args.png_path,
            '/home/opc/email_venv/email_png',
        )
        time.sleep(.5)
        commands.trasfer_file_to_remote(
            conn,
            args.pdf_path,
            '/home/opc/email_venv/pdf_attach',
        )
        time.sleep(.5)
        c1, c2, = commands.create_send_email_commands(
            args.html_path,
            args.csv_or_excel_path,
            args.pdf_path,
        )
        time.sleep(.5)
        commands.run_remote_command_in_shell(conn, c1)
        time.sleep(.5)
        commands.run_remote_command_in_shell(conn, c2)
        #print(conn.run('dir'))
