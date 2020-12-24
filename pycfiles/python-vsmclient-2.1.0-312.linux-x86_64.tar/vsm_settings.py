# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/vsm_settings.py
# Compiled at: 2016-06-13 14:11:03
"""
VSM Settings interface.
"""
import urllib
from vsmclient import base

class VsmSetting(base.Resource):
    """"""

    def __repr__(self):
        return '<VsmSetting: %s>' % self.id


class VsmSettingsManager(base.ManagerWithFind):
    """
    Manage :class:`VsmSetting` resources.
    """
    resource_class = VsmSetting

    def get(self, name):
        """
        Get a vsm setting by name.

        :param name: the setting name.
        """
        qparams = {}
        if name:
            qparams['name'] = name
        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        return self._get('/vsm_settings/get_by_name%s' % query_string, 'setting')

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all vsm settings.

        :rtype: list of :class:`VsmSettings`
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        detail = ''
        if detailed:
            detail = '/detail'
        ret = self._list('/vsm_settings%s%s' % (detail, query_string), 'settings')
        return ret

    def create(self, settings=None):
        """
        Create vsm settings.
        Param: a list of vsm settings.
        """
        body = {'setting': settings}
        return self._create('/vsm_settings', body, 'setting')