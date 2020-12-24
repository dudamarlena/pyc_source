# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tgsociable/gibeplugin.py
# Compiled at: 2007-03-25 11:11:17
try:
    from gibe.plugin import Plugin
except ImportError:
    Plugin = None

if Plugin:
    from tgsociable import SociableWidget

    class SociablePlugin(Plugin):
        __module__ = __name__

        def __init__(self):
            self.reconfigure()

        def reconfigure(self):
            extra_sites = {'muti': {'favicon': 'http://muti.co.za/images/favicon.ico', 'url': 'http://muti.co.za/submit?url=PERMALINK&title=TITLE'}}
            self.tgsw = SociableWidget(extra_sites=extra_sites, active_sites=['muti', 'del.icio.us'])

        def post_top_widgets(self, post, wl):
            wl.extend([self.tgsw])