# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\DataResourcePlugin.py
# Compiled at: 2018-05-17 15:54:05
# Size of source mod 2**32: 2387 bytes
from yapsy.IPlugin import IPlugin
viewTypes = ['ListView', 'TreeView', '']

class DataResourcePlugin(IPlugin):

    def __init__(self, flags=None, **config):
        """
        Config keys should follow RFC 3986 URI format:
            scheme:[//[user[:password]@]host[:port]][/path][?query][#fragment]

        Should provide the abstract methods required of QAbstractItemModel. While this plugin does not depend on Qt, it
        mimics the same functionality, and so can easily be wrapped in a QAbstractItemModel for GUI views. A parent
        model assigns itself to self.model
        """
        super(DataResourcePlugin, self).__init__()
        self.model = None
        self.config = config
        self.flags = flags if flags else {'isFlat':True,  'canPush':False}

    def pushData(self, *args, **kwargs):
        raise NotImplementedError

    def dataChanged(self, topleft=None, bottomright=None):
        if self.model:
            self.model.dataChanged.emit(topleft, bottomright)

    def columnCount(self, index=None):
        raise NotImplementedError

    def rowCount(self, index=None):
        raise NotImplementedError

    def data(self, index, role):
        raise NotImplementedError

    def headerData(self, column, orientation, role):
        raise NotImplementedError

    def index(self, row, column, parent):
        raise NotImplementedError

    def parent(self, index):
        raise NotImplementedError

    @property
    def host(self):
        return self.config['host']

    @property
    def path(self):
        return self.config['path']

    def refresh(self):
        pass


try:
    from qtpy.QtCore import *

    class DataSourceListModel(QAbstractListModel):

        def __init__(self, dataresource):
            super(DataSourceListModel, self).__init__()
            self.dataresource = dataresource
            self.dataresource.model = self
            self.rowCount = dataresource.rowCount
            self.data = dataresource.data
            self.columnCount = dataresource.columnCount
            self.refresh = dataresource.refresh

        @property
        def config(self):
            return self.dataresource.config


except ImportError:
    pass