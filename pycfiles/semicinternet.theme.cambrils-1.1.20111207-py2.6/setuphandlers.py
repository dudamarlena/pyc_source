# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/semicinternet/theme/cambrils/setuphandlers.py
# Compiled at: 2011-06-29 12:34:15


def setupVarious(context):
    if context.readDataFile('semicinternet.theme.cambrils_various.txt') is None:
        return
    else:
        return


def uninstallVarious(context):
    if context.readDataFile('semicinternet.theme.cambrils_uninstall.txt') is None:
        return
    else:
        return