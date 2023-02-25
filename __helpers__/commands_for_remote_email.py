#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 18:08:28 2023

@author: dale
"""

import json

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
                return {'\\"' + k + '\\"': sanitize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [sanitize(elem) for elem in obj]
            else:
                return f'"{obj}"'
        return self.encoder(sanitize(obj))
    
def create_send_email_commands(*args, **kwargs):
    main_dir = r'/home/opc/email_venv'
    helpers_dir = r'/home/opc/email_venv/__helpers__'
    # Serialize kwargs as a JSON string
    kwargs_str = json.dumps(kwargs, 
                            separators=(',', ':'),
                            cls=DoubleQuoteJSONEncoder
                            )
    command = [
    'cat', 'email_venv/compose_email.py' 
#    '--version'
    ]
    command_str = ' '.join(command)
    conn.run('cd /home/opc/email_venv && ls -a', hide=True, echo=True)
    result = conn.run(command_str, hide=True, echo=True)

    if result.failed:
        print('This is printing because it didnt work')
        #print(result.stderr)
    else:
        print(result.stdout)
        print('\nThis is printing because it should have worked?')