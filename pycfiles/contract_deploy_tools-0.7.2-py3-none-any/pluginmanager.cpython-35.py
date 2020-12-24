# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/pluginmanager.py
# Compiled at: 2015-12-16 10:04:32
# Size of source mod 2**32: 1624 bytes
import logging, imp, sys
from .database import Database
from . import config
logger = logging.getLogger(config.APP_NAME)

class PluginManager:

    def __init__(self):
        self.dapps = {}

    def load(self, pname, chain, db, dht, api):
        logger.pluginfo('Plugging dapp "%s"', pname.lower())
        dapp = imp.load_source(pname, config.DATA_DIR + '/dapps/' + pname + '/dapp/__init__.py')
        pc = eval('dapp.' + pname + '.' + pname)
        po = pc(chain, Database.new(config.DATA_DIR + '/dapps/state_' + pname + '_' + chain.getChainCode() + '.dat'), dht, api)
        rpcm = po.getAPI().getRPCMethods()
        for m in rpcm:
            api.registerRPCMethod(pname.lower() + '.' + m, rpcm[m])

        self.dapps[pname.lower()] = po

    def shouldBeHandled(self, m):
        for p in self.dapps:
            if m.DappCode == self.dapps[p].DappCode:
                return True

        return False

    def handleMessage(self, m):
        for p in self.dapps:
            if m.DappCode == self.dapps[p].DappCode:
                logger.pluginfo('Found handler %s for message %s from %s', p, m.Hash, m.Player)
                try:
                    return self.dapps[p].handleMessage(m)
                except Exception as e:
                    logger.critical('Exception from dapp ' + p + ' while handling a message')
                    logger.critical(e)
                    return

        logger.error('Cannot handle message method %d for dapp %s', m.Method, str(m.DappCode))