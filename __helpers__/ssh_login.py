#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 09:41:54 2023

@author: dale
"""

import os
import json
import subprocess
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


def ssh_login_and_run_function(func_to_run, *args, **kwargs):
    path_to_ssh = os.environ.get('SSH_PATH')
    hostname = os.environ.get('VM_HOST')
    # Serialize args and kwargs as JSON strings
    args_str = json.dumps(args, cls=DoubleQuoteJSONEncoder)
    kwargs_str = json.dumps(kwargs, cls=DoubleQuoteJSONEncoder)
    # Build the SSH command to execute the function
    command = f'''ssh -i -T {path_to_ssh} opc@{hostname} "cd /home/opc/email_venv && python3.11 -c "import json, sys; sys.path.append('.'); kwargs = json.loads('{kwargs_str}'); from {func_to_run.__module__} import {func_to_run.__name__};{func_to_run.__name__}(*{args_str}, **kwargs)""'''
    # Run the SSH command and capture its output
    result = subprocess.run(
        [command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        input=b'exit\n',
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr.decode('utf-8')}")
    else:
  #      print(result.stdout.decode('utf-8'))
        print('\nThis is printing becuase it should have worked?')

if __name__ == '__main__':
    def test_func(str_var='This Is A Test'):
        print(str_var + str_var)
    ssh_login_and_run_function(test_func, 'Hello, world! ')
