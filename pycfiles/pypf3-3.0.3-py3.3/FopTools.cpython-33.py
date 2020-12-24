# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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