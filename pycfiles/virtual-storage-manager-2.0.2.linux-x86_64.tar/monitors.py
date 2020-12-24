# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/monitors.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging, time
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'monitors'

    def basic(self, mon):
        LOG.info('mon api view %s ' % mon)
        return {'monitor': {'id': mon['id'], 
                       'name': mon['name'], 
                       'address': mon.get('address'), 
                       'health': mon.get('health'), 
                       'details': mon.get('details')}}

    def show(self, mon):
        LOG.info('mon api view %s ' % mon)
        _mon = {'monitor': {'id': mon['id'], 
                       'name': mon['name'], 
                       'address': mon.get('address'), 
                       'health': mon.get('health'), 
                       'details': mon.get('details'), 
                       'skew': float(mon.get('skew')), 
                       'latency': float(mon.get('latency')), 
                       'kb_total': mon.get('kb_total'), 
                       'kb_used': mon.get('kb_used'), 
                       'kb_avail': mon.get('kb_avail'), 
                       'avail_percent': mon.get('avail_percent')}}
        try:
            _mon['monitor']['updated_at'] = mon.get('updated_at').strftime('%Y-%m-%d %H:%M:%S')
        except:
            _mon['monitor']['updated_at'] = ''

        return _mon

    def index(self, mons):
        """Show a list of mons without many details."""
        return self._list_view(self.basic, mons)

    def detail(self, mons):
        return self._list_view(self.show, mons)

    def _list_view(self, func, mons):
        """Provide a view for a list of mons."""
        mon_list = [ func(mon)['monitor'] for mon in mons ]
        mons_dict = dict(monitors=mon_list)
        return mons_dict