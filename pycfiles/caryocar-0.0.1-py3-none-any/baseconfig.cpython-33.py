# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cary/baseconfig.py
# Compiled at: 2015-08-04 08:06:29
# Size of source mod 2**32: 1382 bytes
import logging
WORKSPACE_DIR = None
SHOULD_RESPOND = False
SHOULD_CLEAN_UP = False
FROM_ADDRESS = None
LOG_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
LOG_FILE = None
LOG_LEVEL = logging.INFO
from cary.echocommand import EchoCommand
COMMANDS = {'echo': (EchoCommand, {})}
ALLOW_FROM_ADDRESSES = None
SMTP_HOST = None
SMTP_RETURN_ADDRESS = None