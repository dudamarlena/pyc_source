# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/servers/technic.py
# Compiled at: 2013-08-16 22:15:55
import json
from . import JarProvider

class Technic(JarProvider):
    api_base = 'http://solder.technicpack.net/api/modpack/?include=full'
    packs = (
     ('bigdig', 'BigDigServer-v{0}.zip'),
     ('tekkit', 'Tekkit_Server_{0}.zip'),
     ('tekkitlite', 'Tekkit_Lite_Server_{0}.zip'),
     ('voltz', 'Voltz_Server_v{0}.zip'))
    builds = ('recommended', 'latest')

    def work(self):
        self.get(self.api_base, self.handle_data)

    def handle_data(self, data):
        data = json.loads(data)
        base = data['mirror_url']
        for name, server in self.packs:
            mod = data['modpacks'][name]
            title = mod['display_name']
            title = 'Tekkit Classic' if title == 'Tekkit' else title
            for build in self.builds:
                self.add(('Technic', title, build.title()), (None, None, None), base + 'servers/' + name + '/' + server.format(mod[build]))

        self.commit()
        return


ref = Technic