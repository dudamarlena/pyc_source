# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted/plugins/eyefi_plugin.py
# Compiled at: 2012-01-03 19:20:54
from zope.interface import implements
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet
from eyefi.config import glue_config, get_cards, twisted_schemaconfigglue
from eyefi.server import build_site
from eyefi.actions import build_actions
cfg = glue_config()
Options = twisted_schemaconfigglue(cfg)

class EyefiServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'eyefi'
    description = 'EyeFi SDHC+WiFi card server'
    options = Options

    def makeService(self, options):
        cards = get_cards(cfg)
        actions = build_actions(cfg, cards)
        site = build_site(cfg, cards, actions)
        server = internet.TCPServer(cfg.get('__main__', 'port'), site)
        return server


serviceMaker = EyefiServiceMaker()