# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/connectrum/svr_info.py
# Compiled at: 2018-11-07 15:05:09
# Size of source mod 2**32: 8290 bytes
from importlib import util as importutil
if importutil.find_spec('bottom') is not None:
    have_bottom = True
else:
    have_bottom = False
import time, random, json
from .constants import DEFAULT_PORTS

class ServerInfo(dict):
    __doc__ = '\n        Information to be stored on a server. Originally based on IRC data published to a channel.\n\n    '
    FIELDS = ['nickname', 'hostname', 'ports', 'version', 'pruning_limit']

    def __init__(self, nickname_or_dict, hostname=None, ports=None, version=None, pruning_limit=None, ip_addr=None):
        if not hostname:
            if not ports:
                super(ServerInfo, self).__init__(nickname_or_dict)
                return
        else:
            self['nickname'] = nickname_or_dict or None
            self['hostname'] = hostname
            self['ip_addr'] = ip_addr or None
            if isinstance(ports, int):
                ports = [
                 't%d' % ports]
            else:
                if isinstance(ports, str):
                    ports = ports.split()
        for p in ports.copy():
            if p[0] == 'v':
                version = p[1:]
                ports.remove(p)

        assert ports, 'Must have at least one port/protocol'
        self['ports'] = ports
        self['version'] = version
        self['pruning_limit'] = int(pruning_limit or 0)

    @classmethod
    def from_response(cls, response_list):
        rv = []
        for params in response_list:
            ip_addr, hostname, ports = params
            if ip_addr == hostname:
                ip_addr = None
            rv.append(ServerInfo(None, hostname, ports, ip_addr=ip_addr))

        return rv

    @classmethod
    def from_dict(cls, d):
        n = d.pop('nickname', None)
        h = d.pop('hostname')
        p = d.pop('ports')
        rv = cls(n, h, p)
        rv.update(d)
        return rv

    @property
    def protocols(self):
        rv = set((i[0] for i in self['ports']))
        assert 'p' not in rv, 'pruning limit got in there'
        assert 'v' not in rv, 'version got in there'
        return rv

    @property
    def pruning_limit(self):
        return self.get('pruning_limit', 100)

    @property
    def hostname(self):
        return self.get('hostname')

    def get_port(self, for_protocol):
        """
            Return (hostname, port number, ssl) pair for the protocol.
            Assuming only one port per host.
        """
        if not len(for_protocol) == 1:
            raise AssertionError('expect single letter code')
        else:
            use_ssl = for_protocol in ('s', 'g')
            if 'port' in self:
                return (
                 self['hostname'], int(self['port']), use_ssl)
            rv = next((i for i in self['ports'] if i[0] == for_protocol))
            port = None
            if len(rv) >= 2:
                try:
                    port = int(rv[1:])
                except:
                    pass

        port = port or DEFAULT_PORTS[for_protocol]
        return (
         self['hostname'], port, use_ssl)

    @property
    def is_onion(self):
        return self['hostname'].lower().endswith('.onion')

    def select(self, protocol='s', is_onion=None, min_prune=0):
        return protocol in self.protocols and (self.is_onion == is_onion if is_onion is not None else True) and self.pruning_limit >= min_prune

    def __repr__(self):
        return ('<ServerInfo {hostname} nick={nickname} ports="{ports}" v={version} prune={pruning_limit}>'.format)(**self)

    def __str__(self):
        return self['hostname'].lower()

    def __hash__(self):
        return hash(self['hostname'].lower())


class KnownServers(dict):
    __doc__ = '\n        Store a list of known servers and their port numbers, etc.\n\n        - can add single entries\n        - can read from a CSV for seeding/bootstrap\n        - can read from IRC channel to find current hosts\n\n        We are a dictionary, with key being the hostname (in lowercase) of the server.\n    '

    def from_json(self, fname):
        """
            Read contents of a CSV containing a list of servers.
        """
        with open(fname, 'rt') as (fp):
            for row in json.load(fp):
                nn = ServerInfo.from_dict(row)
                self[str(nn)] = nn

    def from_irc(self, irc_nickname=None, irc_password=None):
        """
            Connect to the IRC channel and find all servers presently connected.

            Slow; takes 30+ seconds but authoritative and current.

            OBSOLETE.
        """
        if have_bottom:
            from .findall import IrcListener
            bot = IrcListener(irc_nickname=irc_nickname, irc_password=irc_password)
            results = bot.loop.run_until_complete(bot.collect_data())
            bot.loop.close()
            self.update(results)
        else:
            return False

    def add_single(self, hostname, ports, nickname=None, **kws):
        """
            Explicitly add a single entry.
            Hostname is a FQDN and ports is either a single int (assumed to be TCP port)
            or Electrum protocol/port number specification with spaces in between.
        """
        nickname = nickname or hostname
        self[hostname.lower()] = ServerInfo(nickname, hostname, ports, **kws)

    def add_peer_response(self, response_list):
        additions = set()
        for params in response_list:
            ip_addr, hostname, ports = params
            if ip_addr == hostname:
                ip_addr = None
            g = self.get(hostname.lower())
            nickname = g['nickname'] if g else None
            here = ServerInfo(nickname, hostname, ports, ip_addr=ip_addr)
            self[str(here)] = here
            if not g:
                additions.add(str(here))

        return additions

    def save_json(self, fname='servers.json'):
        """
            Write out to a CSV file.
        """
        rows = sorted(self.keys())
        with open(fname, 'wt') as (fp):
            json.dump([self[k] for k in rows], fp, indent=1)

    def dump(self):
        return '\n'.join((repr(i) for i in self.values()))

    def select(self, **kws):
        """
            Find all servers with indicated protocol support. Shuffled.

            Filter by TOR support, and pruning level.
        """
        lst = [i for i in self.values() if (i.select)(**kws)]
        random.shuffle(lst)
        return lst


if __name__ == '__main__':
    ks = KnownServers()
    ks.from_irc()
    from constants import PROTOCOL_CODES
    print('%3d: servers in total' % len(ks))
    for tor in (False, True):
        for pp in PROTOCOL_CODES.keys():
            ll = ks.select(pp, is_onion=tor)
            print('%3d: %s' % (len(ll), PROTOCOL_CODES[pp] + (' [TOR]' if tor else '')))