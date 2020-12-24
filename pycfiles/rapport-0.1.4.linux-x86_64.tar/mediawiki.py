# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/plugins/mediawiki.py
# Compiled at: 2013-05-14 04:37:04
"""
Mediawiki plugin.
"""
import json, requests, rapport.plugin

class MediawikiPlugin(rapport.plugin.Plugin):

    def __init__(self, *args, **kwargs):
        super(MediawikiPlugin, self).__init__(*args, **kwargs)

    def _get(self, params={}):
        params.update({'format': 'json', 'action': 'query'})
        response = requests.get(self.url.geturl(), params=params, auth=(self.login, self.password))
        return json.loads(response.text)['query']

    def collect(self, timeframe):
        edits = self._get({'list': 'usercontribs', 'ucuser': ('{0}').format(self.login), 
           'ucstart': timeframe.end.isoformat() + 'Z', 
           'ucend': timeframe.start.isoformat() + 'Z'})
        return self._results({'edits': edits['usercontribs']})


rapport.plugin.register('mediawiki', MediawikiPlugin)