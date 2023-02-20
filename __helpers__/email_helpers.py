#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:38:22 2023

@author: dale
"""

import base64
import pandas as pd
from html import escape
from pathlib import Path



class GetFiles:
    """ Class for managing the loading of values for the email client"""

    def __init__(self, file_path, *args, **kwargs):
        self._file_path = Path(file_path)
        if not self._file_path.is_file():
            raise ValueError(
                'The selected item is not an file or does not exist.'
            )
        else:
            self.filename = GetFiles.return_only_file_name(file_path)
            self.data = GetFiles.check_file_and_return_values(
                file_path,
                *args,
                **kwargs
            )

    # The read_csv function will need to be modifed
    @staticmethod
    def read_csv_file(file_path, *args, **kwargs) -> pd.DataFrame:
        return pd.read_csv(str(file_path), *args, **kwargs)

    # The read_excel function will need to be modifed
    @staticmethod
    def read_excel_file(file_path, *args, **kwargs) -> pd.DataFrame:
        return pd.read_excel(str(file_path), *args, **kwargs)

    # This is fallback function if the filetype is not in SPECIFIED_IMPORTS
    @staticmethod
    def open_any_file_and_read_contents(file_path: str) -> str:
        with open(file_path, 'r') as f:
            any_file = f.readlines()
            f.close()
        file_str = ''.join(any_file)    
        return file_str
    
    @staticmethod
    def return_only_file_name(file_path):
        return Path(file_path).name
    
    @staticmethod
    def encode_html_str(html_str):
        escaped_html = escape(r"{}".format(html_str))
        return base64.b64encode(escaped_html.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decode_html_str(html_str):
        return base64.b64decode(html_str.encode('utf-8')).decode('utf-8')

    # Update the dictionary when specific file getters are added to Class
    # The stem should be the dictionary key and value is import function
    SPECIFIED_IMPORTS = {
        '.csv': read_csv_file,
        '.xlsx': read_excel_file,
        '.xls': read_excel_file,
    }

    @classmethod
    def check_file_and_return_values(cls, file_path, *args, **kwargs):
        file_suffix= Path(file_path).suffix
        if str(file_suffix) in GetFiles.SPECIFIED_IMPORTS.keys():
            get_func = GetFiles.SPECIFIED_IMPORTS.get(str(file_suffix))
        else:
            get_func = GetFiles.open_any_file_and_read_contents
        return get_func(file_path, *args, **kwargs)
