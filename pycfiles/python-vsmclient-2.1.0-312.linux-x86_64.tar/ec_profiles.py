# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/ec_profiles.py
# Compiled at: 2016-06-13 14:11:03
"""
RBDGroup interface.
"""
import urllib
from vsmclient import base

class ECProfile(base.Resource):
    """A ECProfile is an extra block level storage to the OpenStack instances."""

    def __repr__(self):
        return '<ECProfile: %s>' % self.id


class ECProfilesManager(base.ManagerWithFind):
    """
    Manage :class:`ECProfile` resources.
    """
    resource_class = ECProfile

    def list(self, detailed=True, search_opts=None, paginate_opts=None):
        """
        Get a list of all ECProfile.

        :rtype: list of :class:`ECProfile`
        """
        if search_opts is None:
            search_opts = {}
        if paginate_opts is None:
            paginate_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        for opt, val in paginate_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        detail = ''
        if detailed:
            detail = '/detail'
        ret = self._list('/ec_profiles%s%s' % (detail, query_string), 'ec_profiles')
        return ret

    def ec_profile_create(self, body):
        """
        :param request:
        :param body:{'ec_profiles':[
                            {'name':,#
                            'plugin':,#...
                            ]
                    }
        :return:
        """
        url = '/ec_profiles/ec_profile_create'
        return self.api.client.post(url, body=body)

    def ec_profile_update(self, body):
        """
        :param request:
        :param body:{'ec_profiles':[
                            {'name':,#
                            'plugin':,#
                            'id':,
                            ]
                    }
        :return:
        """
        url = '/ec_profiles/ec_profile_update'
        return self.api.client.post(url, body=body)

    def ec_profiles_remove(self, body):
        """
        :param request:
        :param body:{'ec_profiles':[2,]}
        :return:
        """
        url = '/ec_profiles/ec_profiles_remove'
        return self.api.client.post(url, body=body)