# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/ZopeMonitor/parsers/Munin.py
# Compiled at: 2010-05-18 10:22:39
import re, logging
from Products.ZenUtils.Utils import getExitMessage
from Products.ZenRRD.CommandParser import CommandParser
DELIMITERS = ' :'
MuninParser = re.compile('(\\w+)([%s])([-0-9.]+)' % DELIMITERS)
log = logging.getLogger('Munin')

class Munin(CommandParser):

    def __init__(self, *args, **kw):
        log.debug('Instantiating Munin Parser')

    def processResults(self, cmd, results):
        dps = {}
        output = cmd.result.output
        firstline = output.split('\n')[0].strip()
        exitCode = cmd.result.exitCode
        severity = cmd.severity
        if MuninParser.search(firstline):
            msg, values = '', output
        else:
            msg, values = output, ''
        msg = msg.strip() or 'Cmd: %s - Code: %s - Msg: %s' % (
         cmd.command, exitCode, getExitMessage(exitCode))
        if exitCode != 0:
            results.events.append(dict(device=cmd.deviceConfig.device, summary=msg, severity=severity, message=msg, performanceData=values, eventKey=cmd.eventKey, eventClass=cmd.eventClass, component=cmd.component))
        for line in cmd.result.output.split('\n'):
            match = MuninParser.search(line)
            if match:
                (tag, delimiter, value) = match.groups()
                dps[tag] = float(value)

        for dp in cmd.points:
            if dps.has_key(dp.id):
                results.values.append((dp, dps[dp.id]))