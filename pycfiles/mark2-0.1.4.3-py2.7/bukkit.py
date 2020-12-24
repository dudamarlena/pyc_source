# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/servers/bukkit.py
# Compiled at: 2013-08-16 22:15:55
import json
from . import JarProvider

class Bukkit(JarProvider):

    def work(self):
        self.get('http://dl.bukkit.org/api/1.0/downloads/channels/?_accept=application/json', self.handle_channels)

    def handle_channels(self, data):
        data = json.loads(data)
        for channel in data['results']:
            name = channel['name']
            slug = channel['slug']
            self.add(('Bukkit', name), (None, slug), 'http://dl.bukkit.org/latest-%s/craftbukkit.jar' % slug)

        self.commit()
        return


ref = Bukkit