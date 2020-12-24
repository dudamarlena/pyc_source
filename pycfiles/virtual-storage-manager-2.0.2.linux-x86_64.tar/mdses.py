# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/mdses.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging, time
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'mdses'

    def basic(self, request, mds):
        LOG.info('mdses api view %s ' % mds)
        _mds = {'mds': {'id': mds['id'], 
                   'name': mds['name'], 
                   'gid': mds['gid'], 
                   'state': mds['state'], 
                   'address': mds['address']}}
        _mds['mds']['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(mds['updated_at'], '%Y-%m-%dT%H:%M:%S.000000'))
        return _mds

    def _detail(self, request, mds):
        LOG.info('mdses api detail view %s ' % mds)
        _mds = {'mds': {'id': mds['id'], 
                   'name': mds['name'], 
                   'gid': mds['gid'], 
                   'state': mds['state'], 
                   'address': mds['address']}}
        try:
            _mds['mds']['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(mds['updated_at'], '%Y-%m-%dT%H:%M:%S.000000'))
        except:
            _mds['mds']['updated_at'] = ''

        return _mds

    def detail(self, request, mdses):
        return self._list_view(self._detail, request, mdses)

    def index(self, request, mdses):
        """Show a list of mdses without many details."""
        return self._list_view(self.basic, request, mdses)

    def _list_view(self, func, request, mdses):
        """Provide a view for a list of mdses."""
        mds_list = [ func(request, mds)['mds'] for mds in mdses ]
        mdses_dict = dict(mdses=mds_list)
        return mdses_dict