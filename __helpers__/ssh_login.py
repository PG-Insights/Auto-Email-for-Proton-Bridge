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


def ssh_login_and_run_function(func_to_run, *args, **kwargs):
    path_to_ssh = os.environ.get('SSH_PATH')
    hostname = os.environ.get('VM_HOST')

    # Serialize args and kwargs as JSON strings
    args_str = json.dumps(args)
    kwargs_str = json.dumps(kwargs)

    # Build the SSH command to execute the function
    command = 'python -c "import json, sys; sys.path.append(\'.\'); '
    command += f'args = json.loads(\'{args_str}\'); '
    command += f'kwargs = json.loads(\'{kwargs_str}\'); '
    command += f'from {func_to_run.__module__} import {func_to_run.__name__}; '
    command += f'{func_to_run.__name__}(*args, **kwargs)"'

    # Run the SSH command and capture its output
    result = subprocess.run(
        ["ssh",
         "-i",
         path_to_ssh,
         f"opc@{hostname}",
         '-S',
         '-',
         '-K',
         '-t',
         command,
         ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        input=b'exit\n',
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr.decode('utf-8')}")
    else:
        print(result.stdout.decode('utf-8'))


if __name__ == '__main__':
    def test_func(str_var='This Is A Test'):
        print(str_var + str_var)
    ssh_login_and_run_function(test_func, 'Hello, world! ')
