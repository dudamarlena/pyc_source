# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/mail/interfaces.py
# Compiled at: 2012-03-19 06:23:50
from zope.interface import Interface

class IPrincipalMailInfo(Interface):
    """Principal mail informations interfaces"""

    def getAddresses(self):
        """Get list of mail addresses matching adapted principal
        
        As adapted principal can be a group, result should be a list of
        tuples containing name and address of each target
        """
        pass