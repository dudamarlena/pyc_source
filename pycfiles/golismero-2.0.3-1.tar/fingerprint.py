# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/plugins/generic/fingerprint.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
from lib.core.common import Backend
from lib.core.common import readInput
from lib.core.data import logger
from lib.core.enums import OS
from lib.core.exception import SqlmapUndefinedMethod

class Fingerprint:
    """
    This class defines generic fingerprint functionalities for plugins.
    """

    def __init__(self, dbms):
        Backend.forceDbms(dbms)

    def getFingerprint(self):
        errMsg = "'getFingerprint' method must be defined "
        errMsg += 'into the specific DBMS plugin'
        raise SqlmapUndefinedMethod(errMsg)

    def checkDbms(self):
        errMsg = "'checkDbms' method must be defined "
        errMsg += 'into the specific DBMS plugin'
        raise SqlmapUndefinedMethod(errMsg)

    def checkDbmsOs(self, detailed=False):
        errMsg = "'checkDbmsOs' method must be defined "
        errMsg += 'into the specific DBMS plugin'
        raise SqlmapUndefinedMethod(errMsg)

    def forceDbmsEnum(self):
        pass

    def userChooseDbmsOs(self):
        warnMsg = 'for some reason sqlmap was unable to fingerprint '
        warnMsg += 'the back-end DBMS operating system'
        logger.warn(warnMsg)
        msg = 'do you want to provide the OS? [(W)indows/(l)inux]'
        while True:
            os = readInput(msg, default='W')
            if os[0].lower() == 'w':
                Backend.setOs(OS.WINDOWS)
                break
            elif os[0].lower() == 'l':
                Backend.setOs(OS.LINUX)
                break
            else:
                warnMsg = 'invalid value'
                logger.warn(warnMsg)