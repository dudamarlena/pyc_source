# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/limnoria_github/test.py
# Compiled at: 2020-05-08 12:52:23
# Size of source mod 2**32: 2977 bytes
from supybot.test import *

class GitHubTestCase(PluginTestCase):
    plugins = ('GitHub', 'Config')

    def testAnnounceAdd(self):
        self.assertNotError('config supybot.plugins.GitHub.announces ""')
        self.assertNotError('github announce add #foo ProgVal Limnoria')
        self.assertResponse('config supybot.plugins.GitHub.announces', 'ProgVal/Limnoria | test | #foo')
        self.assertNotError('github announce add #bar ProgVal Supybot-plugins')
        self.assertResponse('config supybot.plugins.GitHub.announces', 'ProgVal/Limnoria | test | #foo || ProgVal/Supybot-plugins | test | #bar')

    def testAnnounceRemove(self):
        self.assertNotError('config supybot.plugins.GitHub.announces ProgVal/Limnoria | test | #foo || ProgVal/Supybot-plugins | #bar')
        self.assertNotError('github announce remove #foo ProgVal Limnoria')
        self.assertResponse('config supybot.plugins.GitHub.announces', 'ProgVal/Supybot-plugins |  | #bar')
        self.assertNotError('github announce remove #bar ProgVal Supybot-plugins')
        self.assertResponse('config supybot.plugins.GitHub.announces', ' ')