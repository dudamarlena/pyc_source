# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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