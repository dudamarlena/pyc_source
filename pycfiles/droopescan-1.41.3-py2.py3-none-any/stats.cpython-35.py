# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/plugins/stats.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 579 bytes
from cement.core import handler, controller
from dscan.common.plugins_util import Plugin, plugins_get
from dscan.common.functions import version_get
from dscan.common import template

class Stats(controller.CementBaseController):

    class Meta:
        label = 'stats'

    @controller.expose(help='shows scanner status & capabilities.')
    def stats(self):
        plugins = plugins_get()
        version = version_get()
        print(template('stats_plugin.mustache', {'version': version, 
         'plugins': plugins}))


def load(app=None):
    handler.register(Stats)