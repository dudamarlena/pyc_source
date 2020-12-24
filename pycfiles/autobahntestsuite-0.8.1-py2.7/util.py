# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/util.py
# Compiled at: 2018-12-17 11:51:20
__all__ = ('AttributeBag', 'Tabify', 'perf_counter')
import json, platform, sys
from datetime import datetime
from twisted.python import log
import autobahn, autobahntestsuite
from autobahn.websocket.utf8validator import Utf8Validator
from autobahn.websocket.xormasker import XorMaskerNull
import time
if not hasattr(time, 'perf_counter'):
    import os
    if os.name == 'nt':
        perf_counter = time.clock
    else:
        perf_counter = time.time
else:
    perf_counter = time.perf_counter

class AttributeBag:

    def __init__(self, **args):
        for attr in self.ATTRIBUTES:
            setattr(self, attr, None)

        self.set(args)
        return

    def serialize(self):
        obj = {}
        for attr in self.ATTRIBUTES:
            obj[attr] = getattr(self, attr)

        return json.dumps(obj)

    def deserialize(self, data):
        obj = json.loads(data)
        self.set(obj)

    def set(self, obj):
        for attr in obj.keys():
            if attr in self.ATTRIBUTES:
                setattr(self, attr, obj[attr])
            elif self.debug:
                log.msg("Warning: skipping unknown attribute '%s'" % attr)

    def __repr__(self):
        s = []
        for attr in self.ATTRIBUTES:
            s.append('%s = %s' % (attr, getattr(self, attr)))

        return self.__class__.__name__ + '(' + (', ').join(s) + ')'


class Tabify:

    def __init__(self, formats, truncate=120, filler=['-', '+']):
        self._formats = formats
        self._truncate = truncate
        self._filler = filler

    def tabify(self, fields=None):
        """
      Tabified output formatting.
      """
        totalLen = 0
        flexIndicators = 0
        flexIndicatorIndex = None
        for i in xrange(len(self._formats)):
            ffmt = self._formats[i][1:]
            if ffmt != '*':
                totalLen += int(ffmt)
            else:
                flexIndicators += 1
                flexIndicatorIndex = i

        if flexIndicators > 1:
            raise Exception('more than 1 flex field indicator')
        totalLen += 3 * (len(self._formats) - 1)
        if totalLen > self._truncate:
            raise Exception('cannot fit content in truncate length %d' % self._truncate)
        r = []
        for i in xrange(len(self._formats)):
            if i == flexIndicatorIndex:
                N = self._truncate - totalLen
            else:
                N = int(self._formats[i][1:])
            if fields:
                s = str(fields[i])
                if len(s) > N:
                    s = s[:N - 2] + '..'
                l = N - len(s)
                m = self._formats[i][0]
            else:
                s = ''
                l = N
                m = '+'
            if m == 'l':
                r.append(s + ' ' * l)
            elif m == 'r':
                r.append(' ' * l + s)
            elif m == 'c':
                c1 = l / 2
                c2 = l - c1
                r.append(' ' * c1 + s + ' ' * c2)
            elif m == '+':
                r.append(self._filler[0] * l)
            else:
                raise Exception('invalid field format')

        if m == '+':
            return (self._filler[0] + self._filler[1] + self._filler[0]).join(r)
        else:
            return (' | ').join(r)
            return


def envinfo():
    res = {}
    res['platform'] = {'hostname': platform.node(), 'os': platform.platform()}
    res['python'] = {'version': platform.python_version(), 'implementation': platform.python_implementation(), 
       'versionVerbose': sys.version.replace('\n', ' ')}
    res['twisted'] = {'version': None, 'reactor': None}
    try:
        import pkg_resources
        res['twisted']['version'] = pkg_resources.require('Twisted')[0].version
    except:
        pass

    try:
        from twisted.internet import reactor
        res['twisted']['reactor'] = str(reactor.__class__.__name__)
    except:
        pass

    v1 = str(Utf8Validator)
    v1 = v1[v1.find("'") + 1:-2]
    v2 = str(XorMaskerNull)
    v2 = v2[v2.find("'") + 1:-2]
    res['autobahn'] = {'version': autobahn.version, 'utf8Validator': v1, 
       'xorMasker': v2, 
       'jsonProcessor': '%s-%s' % (autobahn.wamp.json_lib.__name__, autobahn.wamp.json_lib.__version__)}
    res['autobahntestsuite'] = {'version': autobahntestsuite.version}
    return res


def pprint_timeago(time=False):
    now = datetime.utcnow()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    else:
        if isinstance(time, datetime):
            diff = now - time
        else:
            if not time:
                diff = now - now
            second_diff = diff.seconds
            day_diff = diff.days
            if day_diff < 0:
                return ''
            if day_diff == 0:
                if second_diff < 10:
                    return 'just now'
                if second_diff < 60:
                    return str(second_diff) + ' seconds ago'
                if second_diff < 120:
                    return 'a minute ago'
                if second_diff < 3600:
                    return str(second_diff / 60) + ' minutes ago'
                if second_diff < 7200:
                    return 'an hour ago'
                if second_diff < 86400:
                    return str(second_diff / 3600) + ' hours ago'
            if day_diff == 1:
                return 'Yesterday'
            if day_diff < 7:
                return str(day_diff) + ' days ago'
            if day_diff < 31:
                return str(day_diff / 7) + ' weeks ago'
        if day_diff < 365:
            return str(day_diff / 30) + ' months ago'
    return str(day_diff / 365) + ' years ago'


OPENSSL_HELP = '\nServer key and certificate required for WSS\nTo generate server test key/certificate:\n\nopenssl genrsa -out server.key 2048\nopenssl req -new -key server.key -out server.csr\nopenssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt\n\nThen start wstest:\n\nwstest -m echoserver -w wss://localhost:9000 -k server.key -c server.crt\n'

def _createWssContext(self, options, factory):
    """Create an SSL context factory for WSS connections.
   """
    if not factory.isSecure:
        return
    else:
        try:
            from twisted.internet import ssl
        except ImportError as e:
            print 'You need OpenSSL/pyOpenSSL installed for secure WebSocket(wss)!'
            sys.exit(1)

        if options['key'] is None or options['cert'] is None:
            print OPENSSL_HELP
            sys.exit(1)
        key = str(options['key'])
        cert = str(options['cert'])
        return ssl.DefaultOpenSSLContextFactory(key, cert)