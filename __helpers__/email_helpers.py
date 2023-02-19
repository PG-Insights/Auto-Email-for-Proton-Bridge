#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:38:22 2023

@author: dale
"""
import pandas as pd
from pathlib import Path


class GetFiles:
    """ Class for managing the loading of values for the email client"""
    
    def __init__(self, file_path):
        self._file_path = Path(file_path)
        if not self._file_path.is_file():
            raise ValueError('The selected item is not an accepted file type.')
            
    # The read_csv function will 
    @staticmethod
    def read_csv_file(file_path, *args, **kwargs) -> pd.DataFrame:
        return pd.read_csv(file_path, *args, **kwargs)
    
    # The read_csv function will 
    @staticmethod
    def read_excel_file(file_path, *args, **kwargs) -> pd.DataFrame:
        return pd.read_excel(file_path, *args, **kwargs)
    
    @staticmethod
    def open_any_file_and_read_contents(file_path: str) -> str:
        with open(file_path, 'r') as f:
            any_file = f.read()
            f.close()
        return any_file
    
    # Update the dictionary below if you want to allow more filetypes
    accepted_filetypes = {
        '.csv': read_csv_file,
        '.xlsx': read_excel_file,
        '.xls': read_excel_file,
        }