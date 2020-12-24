# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/oie/KannelMonitor/parsers/Kannel.py
# Compiled at: 2010-09-03 02:46:51
import re, logging
from Products.ZenUtils.Utils import getExitMessage
from Products.ZenRRD.CommandParser import CommandParser
RecvSendQueue = re.compile('([0-9.]+)/([0-9.]+) SMS queued in/out')
RecvSendDeliver = re.compile('([0-9.]+)/([0-9.]+) SMS delivered in/out')
StoreSize = re.compile('store-file ([0-9.]+) bytes')
log = logging.getLogger('Kannel')

class Kannel(CommandParser):

    def __init__(self, *args, **kw):
        log.debug('Instantiating Kannel Parser')

    def processResults(self, cmd, results):
        dps = {}
        output = cmd.result.output
        exitCode = cmd.result.exitCode
        severity = cmd.severity
        recv = sent = recvqueue = sentqueue = storesize = 0
        (msg, values) = ('', '')
        msg = msg.strip() or 'Cmd: %s - Code: %s - Msg: %s' % (
         cmd.command, exitCode, getExitMessage(exitCode))
        if exitCode != 0:
            results.events.append(dict(device=cmd.deviceConfig.device, summary=msg, severity=severity, message=msg, performanceData=values, eventKey=cmd.eventKey, eventClass=cmd.eventClass, component=cmd.component))
        log.info(output)
        match = RecvSendQueue.search(output)
        if match:
            (recvqueue, sentqueue) = match.groups()
        dps['recvqueue'] = int(recvqueue)
        dps['sentqueue'] = int(sentqueue)
        match = RecvSendDeliver.search(output)
        if match:
            (recv, sent) = match.groups()
        dps['recv'] = int(recv)
        dps['sent'] = int(sent)
        match = StoreSize.search(output)
        if match:
            storesize = match.groups()[0]
        dps['storesize'] = int(storesize)
        log.info('recv=%s sent=%s recvqueue=%s sentqueue=%s storesize=%s' % (recv, sent, recvqueue, sentqueue, storesize))
        for dp in cmd.points:
            if dps.has_key(dp.id):
                results.values.append((dp, dps[dp.id]))