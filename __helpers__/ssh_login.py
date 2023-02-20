#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 09:41:54 2023

@author: dale
"""

import os
import json
from fabric import Connection
from dotenv import load_dotenv

load_dotenv()

class DoubleQuoteJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encoder = json.JSONEncoder(
            ensure_ascii=False,
            separators=(',', ':'),
            sort_keys=True
        ).encode

    def encode(self, obj):
        def sanitize(obj):
            if isinstance(obj, dict):
                return {'"' + k + '"': sanitize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [sanitize(elem) for elem in obj]
            else:
                return f'"{obj}"'
        return self.encoder(sanitize(obj))


def ssh_login_and_run_function(func_to_run, **kwargs):
    path_to_ssh = os.environ.get('SSH_PATH')
    hostname = os.environ.get('VM_HOST')

    # Serialize kwargs as a JSON string
    kwargs_str = json.dumps(kwargs, 
                            separators=(',', ':'),
                            cls=DoubleQuoteJSONEncoder
                            )

    # Build the Python command to execute the function
    command = [
        'python3.11', '-c',
        f'import json, sys; sys.path.append("."); kwargs = json.loads(\'{kwargs_str}\'); from {func_to_run.__module__} import {func_to_run.__name__}; {func_to_run.__name__}(**kwargs)'
    ]
    command_str = ' '.join(command)
    print(command_str)
    # Login to the remote machine and execute the command
    with Connection(hostname, 
                    user='opc', 
                    connect_kwargs={'key_filename': path_to_ssh}
                    ) as conn:
        result = conn.run(command_str, hide=True, echo=True)

        if result.failed:
            print('This is printing because it didnt work')
            print(result.stderr)
        else:
            print(result.stdout)
            print('\nThis is printing because it should have worked?')

if __name__ == '__main__':
    def test_func(str_var='This Is A Test'):
        print(str_var + str_var)
    ssh_login_and_run_function(test_func, html='<h2>Hello, world! </h2>')
