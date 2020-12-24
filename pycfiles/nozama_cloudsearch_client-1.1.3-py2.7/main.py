# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nozama/cloudsearch/client/admintool/main.py
# Compiled at: 2013-12-03 06:00:21
"""
The admin tool main as configured in the setup.py

"""
import sys, logging
from .admincmds import AdminCmds

def main():
    """cloudsearch-admin main script as set up in the 'setup.py'."""
    log = logging.getLogger()
    hdlr = logging.StreamHandler()
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)
    log.propagate = False
    while True:
        try:
            app = AdminCmds()
            sys.exit(app.main())
        except KeyboardInterrupt:
            log.info('Exit time.')
            break