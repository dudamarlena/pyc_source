# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\cod6.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'NTAuthority'
__version__ = '0.7'
import b3.parsers.cod4, re

class Cod6Parser(b3.parsers.cod4.Cod4Parser):
    gameName = 'cod6'
    _guidLength = 16
    _commands = {'message': 'tell %(cid)s %(message)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s', 
       'ban': 'clientkick %(cid)s', 
       'unban': 'unbanuser %(name)s', 
       'tempban': 'clientkick %(cid)s'}
    _regPlayer = re.compile('(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<guid>[a-z0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)', re.IGNORECASE)

    def startup(self):
        """
        Called after the parser is created before run().
        """
        b3.parsers.cod4.Cod4Parser.startup(self)
        try:
            self.game.sv_hostname = self.getCvar('sv_hostname').getString().rstrip('/')
            self.debug('sv_hostname: %s' % self.game.sv_hostname)
        except:
            self.game.sv_hostname = None
            self.warning('Could not query server for sv_hostname')

        return

    def pluginsStarted(self):
        """
        Called after the parser loaded and started all plugins.
        """
        self.debug('Admin plugin not patched')

    def OnA(self, action, data, match=None):
        client = self.clients.getByName(data)
        if not client:
            return None
        else:
            actiontype = match.group('type')
            self.verbose('on action: %s: %s' % (client.name, actiontype))
            return self.getEvent('EVT_CLIENT_ACTION', data=actiontype, client=client)