# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/connectrum/findall.py
# Compiled at: 2018-07-30 09:31:35
# Size of source mod 2**32: 4523 bytes
import bottom, random, time, asyncio
from .svr_info import ServerInfo
import logging
logger = logging.getLogger(__name__)

class IrcListener(bottom.Client):

    def __init__(self, irc_nickname=None, irc_password=None, ssl=True):
        self.my_nick = irc_nickname or 
        self.password = irc_password or 
        self.results = {}
        self.servers = set()
        self.all_done = asyncio.Event()
        super(IrcListener, self).__init__(host='irc.freenode.net', port=(6697 if ssl else 6667), ssl=ssl)
        self.on('CLIENT_CONNECT', self.connected)
        self.on('PING', self.keepalive)
        self.on('JOIN', self.joined)
        self.on('RPL_NAMREPLY', self.got_users)
        self.on('RPL_WHOREPLY', self.got_who_reply)
        self.on('client_disconnect', self.reconnect)
        self.on('RPL_ENDOFNAMES', self.got_end_of_names)

    async def collect_data(self):
        self.loop.create_task(self.connect())
        await self.all_done.wait()
        return self.results

    def connected(self, **kwargs):
        logger.debug('Connected')
        self.send('NICK', nick=(self.my_nick))
        self.send('USER', user=(self.my_nick), realname='Connectrum Client')
        self.send('JOIN', channel='#electrum')

    def keepalive(self, message, **kwargs):
        self.send('PONG', message=message)

    async def joined(self, nick=None, **kwargs):
        logger.debug('Joined: %r' % kwargs)
        if nick != self.my_nick:
            await self.add_server(nick)

    async def got_who_reply(self, nick=None, real_name=None, **kws):
        """
            Server replied to one of our WHO requests, with details.
        """
        nick = nick[2:] if nick[0:2] == 'E_' else nick
        host, ports = real_name.split(' ', 1)
        self.servers.remove(nick)
        logger.debug("Found: '%s' at %s with port list: %s", nick, host, ports)
        self.results[host.lower()] = ServerInfo(nick, host, ports)
        if not self.servers:
            self.all_done.set()

    async def got_users(self, users=[], **kws):
        logger.debug('Got %d (more) users in channel', len(users))
        for nick in users:
            await self.add_server(nick)

    async def add_server(self, nick):
        if nick.startswith('E_'):
            self.servers.add(nick[2:])

    async def who_worker(self):
        logger.debug('who task starts')
        copy = self.servers.copy()
        for nn in copy:
            logger.debug('do WHO for: ' + nn)
            self.send('WHO', mask=('E_' + nn))

        logger.debug('who task done')

    def got_end_of_names(self, *a, **k):
        logger.debug('Got all the user names')
        assert self.servers, 'No one on channel!'
        self.loop.create_task(self.who_worker())

    async def reconnect(self, **kwargs):
        logger.warn('Disconnected (will reconnect)')
        time.sleep(3)
        self.loop.create_task(self.connect())
        logger.debug('Reconnect scheduled.')


if __name__ == '__main__':
    import logging
    logging.getLogger('bottom').setLevel(logging.DEBUG)
    logging.getLogger('connectrum').setLevel(logging.DEBUG)
    logging.getLogger('asyncio').setLevel(logging.DEBUG)
    bot = IrcListener(ssl=False)
    bot.loop.set_debug(True)
    fut = bot.collect_data()
    rv = bot.loop.run_until_complete(fut)
    print(rv)