# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/servers/feed_the_beast.py
# Compiled at: 2013-08-16 22:15:55
import re
from hashlib import md5
from xml.dom import minidom
from . import JarProvider

class FeedTheBeast(JarProvider):
    base = 'http://www.creeperrepo.net/'

    def work(self):
        self.get(self.base + 'getdate', self.handle_date)

    def handle_date(self, data):
        hash = md5()
        hash.update('mcepoch1' + data)
        self.token = hash.hexdigest()
        self.get(self.base + 'static/FTB2/modpacks.xml', self.handle_packs)

    def handle_packs(self, data):
        attr = lambda n, name: n.attributes[name].value
        dom = minidom.parseString(data)
        for node in dom.getElementsByTagName('modpack'):
            filename = attr(node, 'serverPack')
            if filename == '':
                continue
            artifact = attr(node, 'name')
            artifact = re.sub(' Pack$', '', artifact)
            artifact = re.sub('^Feed The Beast ', '', artifact)
            artifact = re.sub('^FTB ', '', artifact)
            url = self.base + 'direct/FTB2/' + self.token + '/'
            url += ('^').join((
             'modpacks',
             attr(node, 'dir'),
             attr(node, 'version').replace('.', '_'),
             filename))
            self.add(('Feed The Beast', artifact), ('ftb', None), url)

        self.commit()
        return


ref = FeedTheBeast