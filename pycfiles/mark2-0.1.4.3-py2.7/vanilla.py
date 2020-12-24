# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/servers/vanilla.py
# Compiled at: 2013-08-16 22:15:55
import json
from . import JarProvider

class Vanilla(JarProvider):
    base = 'http://s3.amazonaws.com/Minecraft.Download/versions/'

    def work(self):
        self.get(self.base + 'versions.json', self.handle_data)

    def handle_data(self, data):
        for k, v in json.loads(data)['latest'].iteritems():
            self.add(('Vanilla', k.title()), (None, None), ('{0}{1}/minecraft_server.{1}.jar').format(self.base, v))

        self.commit()
        return


ref = Vanilla