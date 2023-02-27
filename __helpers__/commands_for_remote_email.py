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
                               csv_or_excel_path: str,
                               png_path: str,
                               pdf_path: str) -> tuple:
    from pathlib import Path
    main_dir = Path('/home/opc/email_venv')
    html_dir = Path(main_dir, 'html_files')
    html_path = Path(html_dir, Path(html_path).name)
    csv_dir = Path(main_dir, 'email_lists')
    csv_or_excel_path = Path(csv_dir, Path(csv_or_excel_path).name)
    pdf_dir = Path(main_dir, 'pdf_attach')
    pdf_path = Path(pdf_dir, Path(pdf_path).name)
    png_dir = Path(main_dir, 'email_png')
    png_path = Path(png_dir, Path(png_path).name)
    command_activate_venv_command = " ".join(
        ['source',
         f'{str(main_dir)}/bin/activate'
         ]
        )
    command_send_html_email = " ".join(
        [
            'python3.11',
            f'"{str(main_dir)}/__helpers__/compose_email.py"',
            f'"{str(html_path)}"',
            f'"{str(csv_or_excel_path)}"',
            f'"{str(png_path)}"',
            f'"{str(pdf_path)}"',
        ]
    )
    command_clear_folders = " ".join(
        [
            'rm',
            f'"{str(html_dir)}/*"',
            '&&',
            'rm'
            f'"{str(png_dir)}/*"',
            '&&',
            'rm',
            f'"{str(pdf_dir)}/*"',
        ]
    )
    return (
        command_activate_venv_command,
        command_send_html_email,
        command_clear_folders,

    )
