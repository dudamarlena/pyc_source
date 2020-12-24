# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/frontends/frontend.py
# Compiled at: 2007-12-02 16:26:54
import os, string
from config import Config
from salamoia.h2o.decorators.lazy import *
installedFrontends = {}
server = 'n'
__optionProcessingDone = False

def prepareOptionProcessing(cls):
    global __optionProcessingDone
    if __optionProcessingDone:
        return
    if not cls.optionParser:
        from optparse import OptionParser
        cls.optionParser = OptionParser()
    optionParser = cls.optionParser
    optionParser.add_option('-c', '--configfile', action='store', type='string', dest='config', default=None, help='read configuration from this file')
    optionParser.add_option('-e', '--embedded', action='store_true', dest='embedded', default=False, help='use embedded nacl')
    __optionProcessingDone = True
    return


class Frontend:
    __module__ = __name__
    optionParser = None

    def __init__(self):
        None
        return

    @classmethod
    def start(cls):
        prepareOptionProcessing(cls)
        frontend = cls()
        group = frontend.options(frontend.optionParser)
        frontend.optionParser.add_option_group(group)
        (options, args) = frontend.optionParser.parse_args()
        frontend.options = options
        frontend.args = args
        if options.config:
            Config.setConfigFile(options.config)
        frontend.run()

    def defaultFrontend(cls):
        """
        Obsolete
        """
        prepareOptionProcessing(cls)
        frontend_names = installedFrontends.keys()
        default = 'qt ncurses ashella cli oliva sansa'
        (options, args) = cls.optionParser.parse_args()
        conf = options.frontends
        if options.profile:
            from client import Client
            Client.setDefaultProfile(options.profile)
        if options.config:
            Config.setConfigFile(options.config)
        if not conf:
            conf = os.getenv('SALAMOIA_FRONTENDS')
        if not conf:
            cfg = Config()
            conf = cfg.get('General', 'Frontends', default)
        preferred_names = conf.split()
        for i in preferred_names:
            if i in frontend_names:
                if installedFrontends[i].checkEnv():
                    return installedFrontends[i]

        return

    defaultFrontend = classmethod(defaultFrontend)

    def addFrontend(cls, frontend):
        installedFrontends[frontend.name()] = frontend

    addFrontend = classmethod(addFrontend)

    def checkEnv(self):
        if self.requiresGui() and not os.getenv('DISPLAY'):
            return False
        return True

    def requiresGui(self):
        return False

    def requiresTty(self):
        return False

    def options(self, parser):
        cfg = Config.defaultConfig()
        from optparse import OptionGroup
        optionGroup = OptionGroup(parser, 'Default Options')
        return optionGroup

    def run(self):
        print 'error: sublcass shoud implement run method'