# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/filerouter.py
# Compiled at: 2010-12-12 22:28:56
import fileutils
from conf import settings

class router:

    def moveFile(self, source_file, destination_location):
        fileutils.moveFile(source_file, destination_location)

    def moveUsed(self, file_name):
        if settings.DEBUG:
            print 'moving ', file_name, 'to', settings.USEDFILES_PATH
        fileutils.moveFile(file_name, settings.USEDFILES_PATH)

    def moveFailed(self, fileName):
        fileutils.moveFile(fileName, settings.FAILEDFILES_PATH)