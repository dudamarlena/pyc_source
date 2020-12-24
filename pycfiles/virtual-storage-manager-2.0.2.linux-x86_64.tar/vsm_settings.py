# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/vsm_settings.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'settings'

    def __init__(self):
        pass

    def basic(self, request, setting):
        return {'setting': {'id': setting.get('id'), 
                       'name': setting.get('name'), 
                       'value': setting.get('value')}}

    def _detail(self, request, setting):
        return {'setting': {'id': setting['id'], 
                       'name': setting['name'], 
                       'value': setting['value'], 
                       'default_value': setting['default_value']}}

    def detail(self, request, settings):
        return self._list_view(self._detail, request, settings)

    def index(self, request, settings):
        """Show a list of vsm settings without many details."""
        return self._list_view(self.basic, request, settings)

    def _list_view(self, func, request, settings):
        """Provide a view for a list of vsm settings."""
        s_list = [ func(request, setting)['setting'] for setting in settings ]
        s_dict = dict(settings=s_list)
        return s_dict