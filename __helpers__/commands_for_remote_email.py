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
        conn.run(command_str, asynchronous=False)


def create_send_email_commands(html_path: str,
                               csv_or_excel_path: str) -> tuple:
    from pathlib import Path
    main_dir = Path('/home/opc/email_venv')
    html_dir = Path(main_dir, 'html_files')
    html_path = Path(html_dir, Path(html_path).name)
    csv_dir = Path(main_dir, 'email_lists')
    csv_or_excel_path = Path(csv_dir, Path(csv_or_excel_path).name)
    command_activate_venv_command = " ".join(
        ['source', 
         f'"{str(main_dir)}/bin/activate"'])
    command_send_html_email = " ".join([
        'python3.11',
        f'"{main_dir}/__helpers__/compose_email.py"',
        f'"{html_path}"',
        f'"{csv_or_excel_path}"',
    ]
    )
    return (
        command_activate_venv_command,
        command_send_html_email

    )
