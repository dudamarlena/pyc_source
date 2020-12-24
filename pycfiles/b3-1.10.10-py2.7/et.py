# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\et.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'ThorN'
__version__ = '0.0.6'
import re, string, b3, b3.clients, b3.events
from b3.functions import prefixText
from b3.parsers.punkbuster import PunkBuster
from b3.parsers.q3a.abstractParser import AbstractParser

class EtParser(AbstractParser):
    gameName = 'et'
    privateMsg = False
    PunkBuster = None
    _logSync = 2
    _commands = {'ban': 'banid %(cid)s %(reason)s', 
       'kick': 'clientkick %(cid)s %(reason)s', 
       'message': 'qsay %(message)s', 
       'say': 'qsay %(message)s', 
       'set': 'set %(name)s %(value)s', 
       'tempban': 'clientkick %(cid)s %(reason)s'}
    _eventMap = {}
    _lineClear = re.compile('^(?:[0-9:.]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<pbid>[0-9A-Z]{32}):\\s*(?P<name>[^:]+):\\s*(?P<num1>[0-9]+):\\s*(?P<num2>[0-9]+):\\s*(?P<ip>[0-9.]+):(?P<port>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<name>.+):\\s+(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+)\\s(?P<acid>[0-9]+)\\s(?P<aweap>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+)\\s(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>.*)$', re.IGNORECASE))

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self.clients.new_client('-1', guid=self.gameName + ':WORLD', name='World', pbid='WORLD', hide=True)
        self.PunkBuster = PunkBuster.PunkBuster(self)
        self._eventMap['warmup'] = self.getEventID('EVT_GAME_WARMUP')
        self._eventMap['restartgame'] = self.getEventID('EVT_GAME_ROUND_END')
        self.debug('Forcing server cvar g_logsync to %s' % self._logSync)
        self.setCvar('g_logsync', self._logSync)

    def OnConnectinfo(self, action, data, match=None):
        guid = match.group('pbid')
        client = self.clients.getByCID(match.group('cid'))
        if client:
            if client.guid == guid:
                if client.exactName != match.group('name'):
                    client.exactName = match.group('name')
                    client.setName(self.stripColors(client.exactName))
                return self.getEvent('EVT_CLIENT_JOIN', client=client)
            self.verbose('disconnect the existing client %s %s => %s %s', match.group('cid'), guid, client.cid, client)
            client.disconnect()
        client = self.clients.newBaseClient()
        client.cid = match.group('cid')
        client.pbid = client.guid = self.gameName + ':' + guid
        client.ip = match.group('ip')
        client.exactName = match.group('name')
        client.name = self.stripColors(client.exactName)
        self.clients.update(client)

    def OnClientuserinfochangedguid(self, action, data, match=None):
        client = self.clients.getByCID(match.group('cid'))
        cid, pbid, data = string.split(data, ' ', 2)
        bclient = self.parseUserInfo(cid + ' ' + data)
        if bclient:
            self.clients.update(bclient, client)

    def OnGib(self, action, data, match=None):
        victim = self.clients.getByCID(match.group('cid'))
        if not victim:
            self.debug('No victim')
            return None
        else:
            attacker = self.clients.getByCID(match.group('acid'))
            if not attacker:
                self.debug('No attacker')
                return None
            event_key = 'EVT_CLIENT_GIB'
            if attacker.cid == victim.cid:
                event_key = 'EVT_CLIENT_GIB_SELF'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team:
                event_key = 'EVT_CLIENT_GIB_TEAM'
            return self.getEvent(event_key, (100, match.group('aweap'), ''), attacker, victim)

    def OnKill(self, action, data, match=None):
        victim = self.clients.getByCID(match.group('cid'))
        if not victim:
            self.debug('No victim')
            return None
        else:
            attacker = self.clients.getByCID(match.group('acid'))
            if not attacker:
                self.debug('No attacker')
                return None
            event_key = 'EVT_CLIENT_KILL'
            if attacker.cid == victim.cid:
                event_key = 'EVT_CLIENT_SUICIDE'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team:
                event_key = 'EVT_CLIENT_KILL_TEAM'
            return self.getEvent(event_key, (100, match.group('aweap'), ''), attacker, victim)

    def OnSayteamc(self, action, data, match=None):
        client = self.clients.getByCID(match.group('cid'))
        if not client:
            self.debug('no client - attempt join')
            return None
        else:
            return self.getEvent('EVT_CLIENT_TEAM_SAY', match.group('text'), client)

    def OnSayc(self, action, data, match=None):
        client = self.clients.getByCID(match.group('cid'))
        if not client:
            self.debug('no client - attempt join')
            return None
        else:
            return self.getEvent('EVT_CLIENT_SAY', match.group('text'), client)

    def message(self, client, text):
        """
        Send a private message to a client.
        :param client: The client to who send the message.
        :param text: The message to be sent.
        """
        if client is None:
            self.say(text)
            return
        else:
            if client.cid is None:
                return
            lines = []
            message = prefixText([self.msgPrefix, self.pmPrefix], text)
            message = message.strip()
            for line in self.getWrap(message):
                lines.append(self.getCommand('message', message=line))

            self.writelines(lines)
            return

    def getNextMap(self):
        pass