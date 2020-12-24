# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/rbd_pools.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging, time
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'rbd_pools'

    def basic(self, request, rbd_pool):
        LOG.info('rbd_pools api view %s ' % rbd_pool)
        rbd = {'rbd_pool': {'id': rbd_pool['id'], 
                        'pool': rbd_pool['pool'], 
                        'image_name': rbd_pool['image'], 
                        'size': rbd_pool['size'], 
                        'objects': rbd_pool['objects'], 
                        'order': rbd_pool['order'], 
                        'format': rbd_pool['format']}}
        rbd['rbd_pool']['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(rbd_pool['updated_at'], '%Y-%m-%dT%H:%M:%S.000000'))
        return rbd

    def _detail(self, request, rbd_pool):
        LOG.info('rbd_pools api detail view %s ' % rbd_pool)
        rbd = {'rbd_pool': {'id': rbd_pool['id'], 
                        'pool': rbd_pool['pool'], 
                        'image_name': rbd_pool['image'], 
                        'size': rbd_pool['size'], 
                        'objects': rbd_pool['objects'], 
                        'order': rbd_pool['order'], 
                        'format': rbd_pool['format']}}
        try:
            rbd['rbd_pool']['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(rbd_pool['updated_at'], '%Y-%m-%dT%H:%M:%S.000000'))
        except:
            rbd['rbd_pool']['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(rbd_pool['created_at'], '%Y-%m-%dT%H:%M:%S.000000'))

        return rbd

    def detail(self, request, rbd_pools):
        return self._list_view(self._detail, request, rbd_pools)

    def index(self, request, rbd_pools):
        """Show a list of rbd_pools without many details."""
        return self._list_view(self.basic, request, rbd_pools)

    def _list_view(self, func, request, rbd_pools):
        """Provide a view for a list of rbd_pools."""
        rbd_pool_list = [ func(request, rbd_pool)['rbd_pool'] for rbd_pool in rbd_pools ]
        rbd_pools_dict = dict(rbd_pools=rbd_pool_list)
        return rbd_pools_dict