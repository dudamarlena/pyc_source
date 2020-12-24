# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/payno/.local/share/virtualenvs/tomwer_venv/lib/python3.7/site-packages/rsyncmanager/utils.py
# Compiled at: 2020-05-04 08:56:52
# Size of source mod 2**32: 1547 bytes
"""
This module is used to manage rsync commands.
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '04/05/2020'

class Borg:
    __doc__ = 'Borg pattern'
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state