#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 09:41:54 2023

@author: dale
"""

import os
from fabric import Connection
from dotenv import load_dotenv

load_dotenv()


def return_ssh_connection(
        path_to_ssh=os.environ.get('SSH_PATH'),
        hostname = os.environ.get('VM_HOST')
        ) -> Connection:
    # Login to the remote machine and return connection
    return Connection(
        hostname, 
        user='opc', 
        connect_kwargs={'key_filename': path_to_ssh}
    ) 


if __name__ == '__main__':
    def test_func(str_var='This Is A Test'):
        print(str_var + str_var)
    
    conn = return_ssh_connection()
    print(conn.is_connected)