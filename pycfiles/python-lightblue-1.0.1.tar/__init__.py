# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lkrajice/Redhat/metaxor/python-lightblue/src/tests/__init__.py
# Compiled at: 2020-03-12 11:20:13
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from lightblue.service import LightBlueService

class FakeLightblueService(LightBlueService):

    def __init__(self, *args, **kwargs):
        self.data_api = Mock()
        self.metadata_api = Mock()
        self.insert_data = Mock()
        self.delete_data = Mock()
        self.update_data = Mock()
        self.find_data = Mock()
        self.get_schema = Mock()