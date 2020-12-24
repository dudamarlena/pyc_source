# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pf3/pdf/FopTools.py
# Compiled at: 2014-08-15 04:10:20
# Size of source mod 2**32: 320 bytes
import logging, traceback, subprocess
COMMASPACE = ', '

class FopTools:
    fop_exec = None
    fop_config = None
    noosh_monitor = None

    def __init__(self, fop_exec, fop_config):
        self.logger = logging.getLogger('pf3')
        self.fop_exec = fop_exec
        self.fop_config = fop_config