# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libcontractvm/DappManager.py
# Compiled at: 2015-12-21 06:08:33
# Size of source mod 2**32: 1628 bytes
import requests, binascii, json, sys, logging, time, signal
from threading import Thread
from threading import Lock
from colorlog import ColoredFormatter
from libcontractvm import Wallet
from libcontractvm import ConsensusManager
from . import Log
logger = logging.getLogger('libcontractvm')

class DappManager:

    def __init__(self, consensusmgr, wallet):
        self.consensusManager = consensusmgr
        self.wallet = wallet

    def produceTransaction(self, method, arguments, bmethod='broadcast'):
        logger.info('Producing transaction: %s %s', method, str(arguments))
        while 1:
            best = self.consensusManager.getBestNode()
            res = self.consensusManager.jsonCall(best, method, arguments)
            txhash = self.wallet.createTransaction([res['outscript']], res['fee'])
            if txhash == None:
                logger.error('Failed to create transaction, retrying in few seconds...')
                time.sleep(10)
                continue
                cid = self.consensusManager.jsonCall(best, bmethod, [txhash, res['tempid']])
                if cid == None:
                    logger.error('Broadcast failed')
                    time.sleep(10)
                    continue
                    cid = cid['txid']
                    if cid != None:
                        logger.info('Broadcasting transaction: %s', cid)
                        return cid
                    logger.error('Failed to produce transaction, retrying in 10 seconds')
                    time.sleep(10)