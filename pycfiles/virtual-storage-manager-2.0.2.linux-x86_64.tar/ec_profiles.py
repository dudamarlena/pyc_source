# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/ec_profiles.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging, time
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'ec_profiles'

    def _detail(self, request, ec_profile):
        LOG.info('ec_profiles api detail view %s ' % ec_profile)
        ec_profile = {'id': ec_profile.id, 
           'name': ec_profile.name, 
           'plugin': ec_profile.plugin, 
           'plugin_path': ec_profile.plugin_path, 
           'pg_num': ec_profile.pg_num, 
           'plugin_kv_pair': ec_profile.plugin_kv_pair}
        return ec_profile

    def detail(self, request, ec_profiles):
        LOG.info('ec_profiles detail view-----%s' % ec_profiles)
        return self._list_view(self._detail, request, ec_profiles)

    def _list_view(self, func, request, ec_profiles):
        """Provide a view for a list of ec_profiles."""
        ec_profile_list = [ func(request, ec_profile) for ec_profile in ec_profiles ]
        ec_profile_dict = dict(ec_profiles=ec_profile_list)
        return ec_profile_dict