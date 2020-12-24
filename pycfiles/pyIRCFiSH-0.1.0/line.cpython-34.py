# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/line.py
# Compiled at: 2015-10-08 05:15:41
# Size of source mod 2**32: 10207 bytes
__doc__ = 'Objects and utilities related to IRC messages.'
import operator, re
from itertools import takewhile
from functools import reduce, lru_cache
from logging import getLogger
_logger = getLogger(__name__)

class Tags:
    """Tags"""
    __slots__ = ('tags', 'tagstr')

    def __init__(self, *, tags=None, tagstr=None):
        self.tags = tags
        self.tagstr = tagstr
        if not self.tags:
            self = self.parse(self.tagstr)

    @classmethod
    def parse(cls, raw):
        """Parse a raw tag string into a Tags object."""
        if not raw:
            _logger.debug('No tags on this message')
            return
        tags = dict()
        for tag in raw.split(';'):
            key, _, value = tag.partition('=')
            if value == '':
                value = None
            tags[key] = value

        return cls(tags=tags, tagstr=raw)

    def __repr__(self):
        return 'Tags(tags={})'.format(repr(self.tags))

    def __str__(self):
        ret = []
        for key, value in self.tags.items():
            if value is None:
                value = ''
            ret.append('{}={}'.format(key, value))

        return ';'.join(ret)


class Hostmask:
    """Hostmask"""
    __slots__ = ('nick', 'username', 'host', 'maskstr')

    def __init__(self, *, nick=None, username=None, host=None, mask=None):
        """Initalise the Hostmask object."""
        self.nick = nick
        self.username = username
        self.host = host
        self.maskstr = mask
        if not self.maskstr:
            str(self)

    @classmethod
    def parse(cls, raw):
        """Parse a raw hostmask into a Hostmask object.

        :param raw:
            The raw hostmask to parse.

        """
        if not raw:
            _logger.debug('No hostmask found')
            return
        else:
            host_sep = raw.find('@')
            if host_sep == -1:
                if raw.find('.') != -1:
                    return cls(host=raw, mask=raw)
                else:
                    return cls(nick=raw, mask=raw)
            nick_sep = raw.find('!')
            has_username = nick_sep != -1
            if not has_username:
                return cls(nick=raw[:host_sep], host=raw[host_sep + 1:], mask=raw)
            return cls(nick=raw[:nick_sep], username=raw[nick_sep + 1:host_sep], host=raw[host_sep + 1:], mask=raw)

    @staticmethod
    @lru_cache(maxsize=128)
    def _compile(string):
        string = re.escape(string)
        string = '^' + string.replace('\\*', '.*').replace('\\?', '.')
        return re.compile(string)

    def match(self, mask):
        """Check if a given mask matches this hostmask."""
        if mask.startswith(('$', '#', '&', '!', '+')):
            raise ValueError('Possible extban detected, naive match impossible')
        mask = Hostmask.parse(mask.lower())
        if mask.nick is not None:
            if self.nick is None:
                return False
            match = self._compile(mask.nick)
            if not match.match(self.nick):
                return False
        if mask.username is not None:
            if self.username is None:
                return False
            match = self._compile(mask.username)
            if not match.match(self.username):
                return False
        if mask.host is not None:
            if self.host is None:
                return False
            match = self._compile(mask.host)
            if not match.match(self.host):
                return False
        return True

    def __str__(self):
        if not self.maskstr:
            if not any((self.nick, self.username, self.host)):
                self.maskstr = ''
            if self.nick and not self.host:
                self.maskstr = self.nick
            else:
                if not self.nick and self.host:
                    self.maskstr = self.host
                else:
                    if self.username:
                        self.maskstr = '{}!{}@{}'.format(self.nick, self.username, self.host)
                    else:
                        self.maskstr = '{}@{}'.format(self.nick, self.host)
        return self.maskstr

    def __bytes__(self):
        return str(self).encode('utf-8', 'replace')

    def __repr__(self):
        return 'Hostmask(nick={}, username={}, host={})'.format(repr(self.nick), repr(self.username), repr(self.host))


class Line:
    """Line"""
    __slots__ = ('tags', 'hostmask', 'command', 'params', 'linestr')
    IN = True
    OUT = False

    def __init__(self, *, tags=None, hostmask=None, command=None, params=None, line=None):
        """Initalise the Line object."""
        self.tags = tags
        self.hostmask = hostmask
        self.command = command
        self.params = params if params is not None else list()
        self.linestr = line
        if isinstance(self.tags, str):
            self.tags = Tags.parse(self.tags)
        if isinstance(self.hostmask, str):
            self.hostmask = Hostmask.parse(self.hostmask)
        if isinstance(self.command, int):
            self.command = str(self.command)
        if self.linestr is None:
            str(self)

    @classmethod
    def parse(cls, line):
        """Parse a raw string into a Line.

        Also should raise on any invalid line.  It will be quite liberal with
        hostmasks (accepting such joys as '' and 'user1@user2@user3'), but
        trying to enforce strict validity in hostmasks will be slow.

        """
        if not line:
            _logger.warning('Blank line passed in!')
            return
        raw_line = line
        tags = None
        hostmask = None
        params = list()
        if line[0] == '@':
            space = line.index(' ')
            tags = Tags.parse(line[1:space])
            line = line[space:].lstrip()
        if line[0] == ':':
            space = line.index(' ')
            hostmask = Hostmask.parse(line[1:space])
            line = line[space:].lstrip()
        command = reduce(operator.concat, takewhile(lambda char: char not in (' ', ':'), line))
        assert len(command) > 0
        line = line[len(command):].lstrip().rstrip('\r\n')
        while len(line) > 0:
            next_param = ''
            line = line.lstrip()
            if not line:
                next_param = ''
                break
            if line[0] == ':':
                next_param = line[1:]
                line = ''
            else:
                next_param = reduce(operator.concat, takewhile(lambda char: char != ' ', line))
                line = line[len(next_param):]
            params.append(next_param)

        return cls(tags=tags, hostmask=hostmask, command=command, params=params, line=raw_line)

    def __str__(self):
        if not self.linestr:
            line = []
            if self.hostmask:
                line.append(':' + str(self.hostmask))
            line.append(self.command)
            if self.params:
                if any(x in (' ', ':') for x in self.params[(-1)]):
                    line.extend(self.params[:-1])
                    line.append(':' + self.params[(-1)])
                else:
                    line.extend(self.params)
            self.linestr = ' '.join([str(x) for x in line]) + '\r\n'
        return self.linestr

    def __bytes__(self):
        return str(self).encode('utf-8', 'replace')

    def __repr__(self):
        return 'Line(tags={}, hostmask={}, command={}, params={})'.format(repr(self.tags), repr(self.hostmask), repr(self.command), repr(self.params))

    def __hash__(self):
        return hash(str(self))