# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/beaker.py
# Compiled at: 2014-10-07 16:12:29
# Size of source mod 2**32: 219 bytes
from hatak.plugin import Plugin

class BeakerPlugin(Plugin):

    def get_include_name(self):
        return 'pyramid_beaker'

    def add_unpackers(self):
        self.unpacker.add('session', lambda req: req.session)