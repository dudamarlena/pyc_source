# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/mainprocessor.py
# Compiled at: 2011-01-03 14:39:55
from synthesis.conf import settings
from synthesis import fileutils
from selector import FileHandler
import os, sys
from synthesis.logger import Logger

class MainProcessor:

    def __init__(self):
        if settings.MODE == 'TEST':
            warningTxt = 'CAUTION: TEST MODE - This wipes DB Clean'
            fileutils.makeBlock(warningTxt)
            warningTxt = "CTRL-C or CTRL-Break to Stop - (waiting before startup, in case you don't want to wipe your existing db)"
            fileutils.makeBlock(warningTxt)
            fileutils.sleep(1)
        if settings.DEBUG:
            if settings.MODE == 'TEST':
                from synthesis import postgresutils
                utils = postgresutils.Utils()
                utils.blank_database()
            os.path.exists(settings.LOGS) or os.mkdir(settings.LOGS)
        elif settings.DEBUG:
            print 'Logs Directory exists:', settings.LOGS
        if len(sys.argv) > 1:
            level = sys.argv[1]
        else:
            level = 0
        debugMessages = Logger(settings.LOGGING_INI, level)
        if settings.DEBUG:
            debugMessages.log('Logging System Online', 0)
        try:
            if settings.DEBUG:
                print 'Now instantiating FileHandler'
            FileHandler()
            print 'calling sys.exit'
            sys.exit
        except KeyboardInterrupt:
            print 'Stopping: KeyboardInterrupt at MainProcessor.py'
            debugMessages.__quit__()
            sys.exit()