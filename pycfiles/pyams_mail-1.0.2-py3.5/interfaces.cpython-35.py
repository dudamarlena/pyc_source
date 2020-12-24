# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_mail/interfaces.py
# Compiled at: 2020-02-20 09:58:33
# Size of source mod 2**32: 1097 bytes
"""PyAMS_mail.interfaces module

This module provides IPrincipalMailInfo, which can return email address(es) or any principal,
if the authentication plug-in provides this information.
"""
from zope.interface import Interface
MAILERS_VOCABULARY_NAME = 'pyams_mail.mailers'

class IPrincipalMailInfo(Interface):
    __doc__ = 'Principal mail informations interfaces'

    def get_addresses(self):
        """Get list of mail addresses matching adapted principal

        As adapted principal can be a group, result should be a list of
        tuples containing name and address of each group member.
        """
        pass