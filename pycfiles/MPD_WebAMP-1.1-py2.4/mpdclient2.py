# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mpd_webamp/mpdclient2.py
# Compiled at: 2007-06-11 06:34:27
import socket

class socket_talker(object):
    __module__ = __name__

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.file = self.sock.makefile('rb+')
        self.current_line = ''
        self.ack = ''
        self.done = True

    def get_line(self):
        if not self.current_line:
            self.current_line = self.file.readline().rstrip('\n')
        if not self.current_line:
            raise EOFError
        if self.current_line == 'OK' or self.current_line.startswith('ACK'):
            self.done = True
        return self.current_line

    def putline(self, line):
        self.file.write('%s\n' % line)
        self.file.flush()
        self.done = False

    def get_pair(self):
        line = self.get_line()
        self.ack = ''
        if self.done:
            if line.startswith('ACK'):
                self.ack = line.split(None, 1)[1]
            return ()
        pair = line.split(': ', 1)
        if len(pair) != 2:
            raise RuntimeError("bogus response: ``%s''" % line)
        return pair


ZERO = 0
ONE = 1
MANY = 2
plitem_delim = [
 'file', 'directory', 'playlist']
commands = {('kill', 0): ('%s', ZERO, '', []), ('outputs', 0): ('%s', MANY, 'outputs', ['outputid']), ('clear', 0): ('%s', ZERO, '', []), ('currentsong', 0): ('%s', ONE, '', []), ('shuffle', 0): ('%s', ZERO, '', []), ('next', 0): ('%s', ZERO, '', []), ('previous', 0): ('%s', ZERO, '', []), ('stop', 0): ('%s', ZERO, '', []), ('clearerror', 0): ('%s', ZERO, '', []), ('close', 0): ('%s', ZERO, '', []), ('commands', 0): ('%s', MANY, 'commands', ['command']), ('notcommands', 0): ('%s', MANY, 'notcommands', ['command']), ('ping', 0): ('%s', ZERO, '', []), ('stats', 0): ('%s', ONE, 'stats', []), ('status', 0): ('%s', ONE, 'status', []), ('play', 0): ('%s', ZERO, '', []), ('playlistinfo', 0): ('%s', MANY, '', plitem_delim), ('playlistid', 0): ('%s', MANY, '', plitem_delim), ('lsinfo', 0): ('%s', MANY, '', plitem_delim), ('update', 0): ('%s', ZERO, '', []), ('listall', 0): ('%s', MANY, '', plitem_delim), ('listallinfo', 0): ('%s', MANY, '', plitem_delim), ('disableoutput', 1): ('%s %d', ZERO, '', []), ('enableoutput', 1): ('%s %d', ZERO, '', []), ('delete', 1): ('%s %d', ZERO, '', []), ('deleteid', 1): ('%s %d', ZERO, '', []), ('playlistinfo', 1): ('%s %d', MANY, '', plitem_delim), ('playlistid', 1): ('%s %d', MANY, '', plitem_delim), ('crossfade', 1): ('%s %d', ZERO, '', []), ('play', 1): ('%s %d', ZERO, '', []), ('playid', 1): ('%s %d', ZERO, '', []), ('random', 1): ('%s %d', ZERO, '', []), ('repeat', 1): ('%s %d', ZERO, '', []), ('setvol', 1): ('%s %d', ZERO, '', []), ('plchanges', 1): ('%s %d', MANY, '', plitem_delim), ('pause', 1): ('%s %d', ZERO, '', []), ('update', 1): ('%s "%s"', ONE, 'update', []), ('listall', 1): ('%s "%s"', MANY, '', plitem_delim), ('listallinfo', 1): ('%s "%s"', MANY, '', plitem_delim), ('lsinfo', 1): ('%s "%s"', MANY, '', plitem_delim), ('add', 1): ('%s "%s"', ZERO, '', []), ('load', 1): ('%s "%s"', ZERO, '', []), ('rm', 1): ('%s "%s"', ZERO, '', []), ('save', 1): ('%s "%s"', ZERO, '', []), ('password', 1): ('%s "%s"', ZERO, '', []), ('move', 2): ('%s %d %d', ZERO, '', []), ('moveid', 2): ('%s %d %d', ZERO, '', []), ('swap', 2): ('%s %d %d', ZERO, '', []), ('swapid', 2): ('%s %d %d', ZERO, '', []), ('seek', 2): ('%s %d %d', ZERO, '', []), ('seekid', 2): ('%s %d %d', ZERO, '', []), ('find', 2): ('%s "%s" "%s"', MANY, '', plitem_delim), ('search', 2): ('%s "%s" "%s"', MANY, '', plitem_delim), ('list', 1): ('%s "%s"', MANY, '', plitem_delim), ('list', 3): ('%s "%s" "%s" "%s"', MANY, '', plitem_delim)}

def is_command(cmd):
    return cmd in [ k[0] for k in commands.keys() ]


def escape(text):
    text = ('\\\\').join(text.split('\\'))
    text = ('\\"').join(text.split('"'))
    return text


def get_command(cmd, args):
    try:
        return commands[(cmd, len(args))]
    except KeyError:
        raise RuntimeError('no such command: %s (%d args)' % (cmd, len(args)))


def send_command(talker, cmd, args):
    args = list(args[:])
    for (i, arg) in enumerate(args):
        if not isinstance(arg, int):
            args[i] = escape(str(arg))

    format = get_command(cmd, args)[0]
    talker.putline(format % tuple([cmd] + list(args)))


class sender_n_fetcher(object):
    __module__ = __name__

    def __init__(self, sender, fetcher):
        self.sender = sender
        self.fetcher = fetcher
        self.iterate = False

    def __getattr__(self, cmd):
        return lambda *args: self.send_n_fetch(cmd, args)

    def send_n_fetch(self, cmd, args):
        getattr(self.sender, cmd)(*args)
        (junk, howmany, type, keywords) = get_command(cmd, args)
        if howmany == ZERO:
            self.fetcher.clear()
            return
        if howmany == ONE:
            return self.fetcher.one_object(keywords, type)
        assert howmany == MANY
        result = self.fetcher.all_objects(keywords, type)
        if not self.iterate:
            result = list(result)
            self.fetcher.clear()
            return result

        def yield_then_clear(it):
            for x in it:
                yield x

            self.fetcher.clear()

        return yield_then_clear(result)


class command_sender(object):
    __module__ = __name__

    def __init__(self, talker):
        self.talker = talker

    def __getattr__(self, cmd):
        return lambda *args: send_command(self.talker, cmd, args)


class response_fetcher(object):
    __module__ = __name__

    def __init__(self, talker):
        self.talker = talker
        self.converters = {}

    def clear(self):
        while not self.talker.done:
            self.talker.current_line = ''
            self.talker.get_line()

        self.talker.current_line = ''

    def one_object(self, keywords, type):
        entity = dictobj()
        if type:
            entity['type'] = type
        while not self.talker.done:
            self.talker.get_line()
            pair = self.talker.get_pair()
            if not pair:
                self.talker.current_line = ''
                return entity
            (key, val) = pair
            key = key.lower()
            if key in keywords and key in entity.keys():
                return entity
            if not type and 'type' not in entity.keys():
                entity['type'] = key
            entity[key] = self.convert(entity['type'], key, val)
            self.talker.current_line = ''

        return entity

    def all_objects(self, keywords, type):
        while 1:
            obj = self.one_object(keywords, type)
            if not obj:
                raise StopIteration
            yield obj
            if self.talker.done:
                raise StopIteration

    def convert(self, cmd, key, val):
        return self.converters.get(cmd, {}).get(key, lambda x: x)(val)


class dictobj(dict):
    __module__ = __name__

    def __getattr__(self, attr):
        return self[attr]

    def __repr__(self):
        return object.__repr__(self).rstrip('>') + ' ..\n' + '  {\n    ' + (',\n    ').join([ '%s: %s' % (k, v) for (k, v) in self.items() ]) + '\n  }>'


class mpd_connection(object):
    __module__ = __name__

    def __init__(self, host, port):
        self.talker = socket_talker(host, port)
        self.send = command_sender(self.talker)
        self.fetch = response_fetcher(self.talker)
        self.do = sender_n_fetcher(self.send, self.fetch)
        self._hello()

    def _hello(self):
        line = self.talker.get_line()
        if not line.startswith('OK MPD '):
            raise RuntimeError("this ain't mpd")
        self.mpd_version = line[len('OK MPD '):].strip()
        self.talker.current_line = ''

    def __getattr__(self, attr):
        if is_command(attr):
            return getattr(self.do, attr)
        raise AttributeError(attr)


def parse_host(host):
    if '@' in host:
        return host.split('@', 1)
    return (
     '', host)


def connect(**kw):
    import os
    port = int(os.environ.get('MPD_PORT', 6600))
    (password, host) = parse_host(os.environ.get('MPD_HOST', 'localhost'))
    kw_port = kw.get('port', 0)
    kw_password = kw.get('password', '')
    kw_host = kw.get('host', '')
    if kw_port:
        port = kw_port
    if kw_password:
        password = kw_password
    if kw_host:
        host = kw_host
    conn = mpd_connection(host, port)
    if password:
        conn.password(password)
    return conn