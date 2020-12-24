# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/rgws.py
# Compiled at: 2016-06-13 14:11:03
"""
RGWs interface.
"""
import urllib
from vsmclient import base

class Rgw(base.Resource):
    """"""

    def __repr__(self):
        return '<Rgw: %s>' % self.id


class RgwManager(base.ManagerWithFind):
    """
    Manage :class:`RGW` resources.
    """
    resource_class = Rgw

    def create(self, host, rgw_instance_name='radosgw.gateway', is_ssl=False, uid='johndoe', display_name='John Doe', email='john@example.comjohn@example.com', sub_user='johndoe:swift', access='full', key_type='swift'):
        """
        Create a rgw.
        :param host:
        :param rgw_instance_name:
        :param is_ssl:
        :param uid:
        :param display_name:
        :param email:
        :param sub_user:
        :param access:
        :param key_type:
        :return:
        """
        body = {'rgw': {'rgw_info': {'server_name': host, 
                                'rgw_instance_name': rgw_instance_name, 
                                'is_ssl': is_ssl}, 
                   'user_info': {'uid': uid, 
                                 'display_name': display_name, 
                                 'email': email, 
                                 'sub_user': sub_user, 
                                 'access': access, 
                                 'key_type': key_type}}}
        return self._create('/rgws', body, 'rgw')