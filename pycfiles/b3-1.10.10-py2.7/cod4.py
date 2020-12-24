# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\cod4.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'ThorN, xlr8or'
__version__ = '1.5.1'
import b3.clients, b3.functions, b3.parsers.cod2, re

class Cod4Parser(b3.parsers.cod2.Cod2Parser):
    gameName = 'cod4'
    IpsOnly = False
    _guidLength = 32
    _commands = {'message': 'tell %(cid)s %(message)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s', 
       'ban': 'banclient %(cid)s', 
       'unban': 'unbanuser %(name)s', 
       'tempban': 'clientkick %(cid)s', 
       'kickbyfullname': 'kick %(cid)s'}
    _regPlayer = re.compile('^\\s*(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<guid>[0-9a-f]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+?)\\s*(?P<ip>(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])):?(?P<port>-?[0-9]{1,5})\\s*(?P<qport>-?[0-9]{1,5})\\s+(?P<rate>[0-9]+)$', re.IGNORECASE | re.VERBOSE)

    def __new__(cls, *args, **kwargs):
        patch_b3_clients()
        return b3.parsers.cod2.Cod2Parser.__new__(cls)

    def pluginsStarted(self):
        """
        Called after the parser loaded and started all plugins.
        """
        self.patch_b3_admin_plugin()
        self.debug('Admin plugin has been patched')

    def OnJt(self, action, data, match=None):
        client = self.getClient(match)
        if not client:
            self.debug('No client - attempt join')
            self.OnJ(action, data, match)
            client = self.getClient(match)
            if not client:
                return
        client.team = self.getTeam(match.group('team'))
        self.debug('%s has just changed team to %s' % (client.name, client.team))
        return

    def OnK(self, action, data, match=None):
        victim = self.getClient(victim=match)
        if not victim:
            self.debug('No victim %s' % match.groupdict())
            self.OnJ(action, data, match)
            return None
        else:
            attacker = self.getClient(attacker=match)
            if not attacker:
                self.debug('No attacker %s' % match.groupdict())
                return None
            if match.group('ateam'):
                attacker.team = self.getTeam(match.group('ateam'))
            if match.group('team'):
                victim.team = self.getTeam(match.group('team'))
            attacker.name = match.group('aname')
            victim.name = match.group('name')
            eventkey = 'EVT_CLIENT_KILL'
            if attacker.cid == victim.cid or attacker.cid == '-1':
                self.verbose2('Suicide detected')
                eventkey = 'EVT_CLIENT_SUICIDE'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team and victim.team and attacker.team == victim.team and match.group('aweap') != 'briefcase_bomb_mp':
                self.verbose2('Teamkill detected')
                eventkey = 'EVT_CLIENT_KILL_TEAM'
            victim.state = b3.STATE_DEAD
            data = (float(match.group('damage')), match.group('aweap'), match.group('dlocation'), match.group('dtype'))
            return self.getEvent(eventkey, data=data, client=attacker, target=victim)

    def unban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Unban a client.
        :param client: The client to unban
        :param reason: The reason for the unban
        :param admin: The admin who unbanned this client
        :param silent: Whether or not to announce this unban
        """
        if self.PunkBuster:
            if client.pbid:
                result = self.PunkBuster.unBanGUID(client)
                if result:
                    admin.message('^3Unbanned^7: %s^7: %s' % (client.exactName, result))
                if admin:
                    variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
                    fullreason = self.getMessage('unbanned_by', variables)
                else:
                    variables = self.getMessageVariables(client=client, reason=reason)
                    fullreason = self.getMessage('unbanned', variables)
                if not silent and fullreason != '':
                    self.say(fullreason)
            elif admin:
                admin.message('%s ^7unbanned but has no punkbuster id' % client.exactName)
        else:
            name = self.stripColors(client.exactName[:15])
            result = self.write(self.getCommand('unban', name=name, reason=reason))
            if admin:
                admin.message(result)

    def sync(self):
        """
        For all connected players returned by self.get_player_list(), get the matching Client
        object from self.clients (with self.clients.get_by_cid(cid) or similar methods) and
        look for inconsistencies. If required call the client.disconnect() method to remove
        a client from self.clients.
        """
        self.debug('Synchronizing clients')
        plist = self.getPlayerList(maxRetries=4)
        self.verbose2('plist: %s' % plist)
        mlist = {}
        for cid, c in plist.iteritems():
            client = self.clients.getByCID(cid)
            if client:
                self.verbose2('client found: %s' % client.name)
                if client.guid and 'guid' in c and not self.IpsOnly:
                    if b3.functions.fuzzyGuidMatch(client.guid, c['guid']):
                        self.debug('in-sync %s == %s', client.guid, c['guid'])
                        mlist[str(cid)] = client
                    else:
                        self.debug('no-sync %s <> %s', client.guid, c['guid'])
                        client.disconnect()
                elif client.ip and 'ip' in c:
                    if client.ip == c['ip']:
                        self.debug('in-sync %s == %s', client.ip, c['ip'])
                        mlist[str(cid)] = client
                    else:
                        self.debug('no-sync %s <> %s', client.ip, c['ip'])
                        client.disconnect()
                else:
                    self.debug('no-sync: no guid or ip found')
            else:
                self.verbose2('no client found for cid: %s' % cid)

        return mlist

    def authorizeClients(self):
        """
        For all connected players, fill the client object with properties allowing to find
        the user in the database (usualy guid, or punkbuster id, ip) and call the
        Client.auth() method.
        """
        players = self.getPlayerList()
        self.verbose('authorizeClients() = %s' % players)
        for cid, p in players.iteritems():
            if self.PunkBuster:
                sp = self.clients.getByGUID(p['guid'])
                if len(p['guid']) < 32:
                    del p['guid']
                if len(p['pbid']) < 32:
                    del p['pbid']
            else:
                sp = self.clients.getByCID(cid)
            if sp:
                sp.ip = p.get('ip', sp.ip)
                sp.pbid = p.get('pbid', sp.pbid)
                if self.IpsOnly:
                    sp.guid = p.get('ip', sp.guid)
                else:
                    sp.guid = p.get('guid', sp.guid)
                sp.data = p
                sp.auth()


def patch_b3_clients():

    def cod4ClientAuthMethod(self):
        if not self.authed and self.guid and not self.authorizing:
            self.authorizing = True
            name = self.name
            ip = self.ip
            pbid = self.pbid
            try:
                inStorage = self.console.storage.getClient(self)
            except KeyError as msg:
                self.console.debug('User not found %s: %s', self.guid, msg)
                inStorage = False
            except Exception as e:
                self.console.error('Auth self.console.storage.getClient(client) - %s' % self, exc_info=e)
                self.authorizing = False
                return False

            if inStorage:
                self.console.bot('Client found in storage %s: welcome back %s', str(self.id), self.name)
                self.lastVisit = self.timeEdit
                if self.pbid == '':
                    self.pbid = pbid
            else:
                self.console.bot('Client not found in the storage %s: create new', str(self.guid))
            self.connections = int(self.connections) + 1
            self.name = name
            self.ip = ip
            self.save()
            self.authed = True
            self.console.debug('Client authorized: [%s] %s - %s', self.cid, self.name, self.guid)
            if self.numBans > 0:
                ban = self.lastBan
                if ban:
                    self.reBan(ban)
                    self.authorizing = False
                    return False
            self.refreshLevel()
            self.console.queueEvent(self.console.getEvent('EVT_CLIENT_AUTH', data=self, client=self))
            self.authorizing = False
            return self.authed
        else:
            return False

    b3.clients.Client.auth = cod4ClientAuthMethod