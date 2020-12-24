# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\pyVb\network\dhcpServers\server.py
# Compiled at: 2013-03-20 09:41:35
from .. import base

class DhcpServer(base.VirtualBoxObject):
    name = property(lambda s: s.getProp('NetworkName'))

    def _getInfo(self):
        _id = self._initId
        for rec in self.cli.manage.list.dhcpservers():
            if rec['NetworkName'] == _id:
                return rec
        else:
            raise Exception(('Interface {!r} not found').format(_id))