# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/enum/shares.py
# Compiled at: 2016-12-29 01:51:56
from impacket.smbconnection import SessionError
from cme.helpers import gen_random_string
import random, string, ntpath

class ShareEnum:

    def __init__(self, connection):
        self.smbconnection = connection.conn
        self.logger = connection.logger
        self.permissions = {}
        self.root = ntpath.normpath('\\' + gen_random_string())

    def enum(self):
        for share in self.smbconnection.listShares():
            share_name = share['shi1_netname'][:-1]
            self.permissions[share_name] = []
            try:
                self.smbconnection.listPath(share_name, '*')
                self.permissions[share_name].append('READ')
            except SessionError:
                pass

            try:
                self.smbconnection.createDirectory(share_name, self.root)
                self.smbconnection.deleteDirectory(share_name, self.root)
                self.permissions[share_name].append('WRITE')
            except SessionError:
                pass

        self.logger.success('Enumerating shares')
        self.logger.highlight(('{:<15} {}').format('SHARE', 'Permissions'))
        self.logger.highlight(('{:<15} {}').format('-----', '-----------'))
        for share, perm in self.permissions.iteritems():
            if not perm:
                self.logger.highlight(('{:<15} {}').format(share, 'NO ACCESS'))
            else:
                self.logger.highlight(('{:<15} {}').format(share, (', ').join(perm)))