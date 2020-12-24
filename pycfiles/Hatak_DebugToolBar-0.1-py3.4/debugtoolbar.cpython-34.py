# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/debugtoolbar.py
# Compiled at: 2014-09-29 16:23:19
# Size of source mod 2**32: 232 bytes
from hatak.plugin import Plugin

class DebugtoolbarPlugin(Plugin):

    def get_include_name(self):
        if self.settings['debug']:
            return 'pyramid_debugtoolbar'
        raise NotImplementedError()