# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arkow/universidad/pfc/collector/tests/data/plugins/hello.py
# Compiled at: 2012-12-04 11:25:07
from collector.core.plugin import PluginRunnable

class PluginHello(PluginRunnable):
    results = ''

    def get_author(self):
        return 'Ariel'

    def get_name(self):
        return 'Hello'

    def run(self):
        self.results = 'Hello world'

    def autorun(self):
        return True

    @property
    def icon(self):
        return ''