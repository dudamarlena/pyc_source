# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/servers/nukkit.py
# Compiled at: 2013-08-16 22:15:55
from . import JarProvider

class Nukkit(JarProvider):
    base = 'http://www.nukkit-project.fr/downloads/'

    def work(self):
        self.add(('Nukkit', 'Stable'), (None, None), self.base + 'craftnukkit')
        self.add(('Nukkit', 'Beta'), (None, None), self.base + 'beta/craftnukkit')
        self.commit()
        return


ref = Nukkit