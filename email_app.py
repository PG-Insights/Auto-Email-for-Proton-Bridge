#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
You must already have an instance of the email_server running on the
same machine, as well as the Proton-Bridge mail client

Created on Sun Feb 19 09:26:48 2023

@author: dale
"""

import sys
from pathlib import Path

MAIN_DIR = Path(__file__).parent
if str(MAIN_DIR) not in sys.path:
    sys.path.append(str(MAIN_DIR))
    sys.path.append(str(Path(MAIN_DIR, '__helpers__')))

import compose_email
from email_helpers import GetFiles
