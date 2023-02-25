#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 18:08:28 2023

@author: dale
"""

from fabric import Connection
    
    
def trasfer_file_to_remote(conn: Connection, 
                           file_path: str, 
                           save_path: str) -> None:
    with conn:
        conn.put(file_path, save_path)
        

def run_remote_command_in_shell(conn: Connection, 
                                command_str: str) -> None:
    with conn:
        conn.run(command_str, shell=True)

    
def create_send_email_commands(html_path: str, 
                               csv_or_excel_path: str) -> tuple:
    from pathlib import Path
    main_dir = Path('/home/opc/email_venv')
    html_dir = Path(main_dir, 'html_files')
    html_path = Path(html_dir, Path(html_path).stem)
    csv_dir = Path(main_dir, 'email_lists')
    csv_or_excel_path = Path(csv_dir, Path(csv_or_excel_path).stem)
    command_move_to_email_venv_dir = ['cd', str(main_dir)]
    command_activate_venv_command = ['source', 'bin/activate']
    command_send_html_email = [
        'python', 
        '__helpers__/compose_email.py',
        str(html_path),
        str(csv_or_excel_path),
        ]
    return (
        command_move_to_email_venv_dir,
        command_activate_venv_command,
        command_send_html_email
        
        )
    