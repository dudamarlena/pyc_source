# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/connectors/static.py
# Compiled at: 2015-05-11 06:46:57
__author__ = 'moshebasanchig'
from hydro.connectors.base_classes import ConnectorBase
from hydro.exceptions import HydroException

class StaticConnector(ConnectorBase):
    """
    implementation of a static file connector
    """

    def __init__(self, conn_definitions):
        super(ConnectorBase, self).__init__()

    def _verify_connection_definitions(self):
        pass

    def _connect(self):
        pass

    def _execute(self, command):
        return command

    def _close(self):
        pass