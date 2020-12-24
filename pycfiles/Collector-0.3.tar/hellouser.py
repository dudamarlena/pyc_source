# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arkow/universidad/pfc/collector/data/user_plugins/hellouser.py
# Compiled at: 2012-12-04 11:25:06
from collector.core.plugin import PluginRunnable
from PyQt4.Qt import qDebug

class PluginHellouser(PluginRunnable):

    def get_author(self):
        return 'Ariel'

    def get_name(self):
        return 'Hello User'

    def run(self):
        qDebug('Hello user!')

    def autorun(self):
        return True

    @property
    def icon(self):
        return ':/browser.png'