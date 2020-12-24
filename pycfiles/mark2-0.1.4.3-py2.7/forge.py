# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/servers/forge.py
# Compiled at: 2013-08-16 22:15:55
from . import JarProvider

class Forge(JarProvider):
    base = 'http://files.minecraftforge.net/minecraftforge/minecraftforge-universal-{0}.zip'

    def work(self):
        for k in ('latest', 'recommended'):
            self.add(('Forge', k.title()), (None, None), self.base.format(k))

        self.commit()
        return


ref = Forge