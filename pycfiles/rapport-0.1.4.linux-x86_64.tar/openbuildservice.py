# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/plugins/openbuildservice.py
# Compiled at: 2013-07-30 09:04:48
"""
Open Build Service plugin.
"""
import lxml.etree, requests, rapport.plugin

class OpenBuildServicePlugin(rapport.plugin.Plugin):

    def __init__(self, *args, **kwargs):
        super(OpenBuildServicePlugin, self).__init__(*args, **kwargs)

    def _get_xml(self, url):
        response = requests.get(url, auth=(self.login, self.password))
        return lxml.etree.fromstring(response.text)

    def collect(self, timeframe):
        user_projects_url = ("{0}/search/project/id?match=person/@userid='{1}'").format(self.url.geturl(), self.login)
        xml_root = self._get_xml(user_projects_url)
        user_projects = [ project.get('name') for project in xml_root.iterfind('.//project') ]
        for project in user_projects:
            pass


rapport.plugin.register('openbuildservice', OpenBuildServicePlugin)