# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/utils.py
# Compiled at: 2017-02-05 18:31:53
# Size of source mod 2**32: 7150 bytes
import time, random, asyncio, functools
from operator import attrgetter
from ipaddress import ip_address
import aiodns
from nicfit import getLogger
log = getLogger(__name__)

class benchmark(object):
    __doc__ = 'A context manager for taking timing blocks of code.'

    def __init__(self, name=None):
        """If *name* is provided the ``__exit__`` method will print this string
        along with the total elapsed time."""
        self.name = name
        self.timer_stats = {}

    def __enter__(self):
        """Returns a dict with the "start" time. By the __exit__ returns the
        keys "end" and "total" contain those times."""
        self.start = time.time()
        self.timer_stats['start'] = self.start
        return self.timer_stats

    def __exit__(self, ty, val, tb):
        end = time.time()
        self.timer_stats['end'] = end
        self.timer_stats['total'] = end - self.start
        if self.name:
            print('%s : %0.3f seconds' % (self.name, self.timer_stats['total']))
        return False


def signalEvent(callbacks, event, *args, **kwargs):
    log.debug('Invoking signal %s' % event)
    if callbacks:
        func = getattr(callbacks, event)
        asyncio.get_event_loop().call_soon((functools.partial)(func, *args, **kwargs))
    else:
        log.debug('No callbacks set')


def stripNsFromTag(tag, ns):
    """Removes ``ns`` from the lxml fully qualified tag name.
    e.g. {namespace}tagname would return tagname."""
    ns_prefix = '{%s}' % ns
    if tag.startswith(ns_prefix):
        return tag[len(ns_prefix):]
    raise ValueError("tag is not in namsepace '%s'" % ns)


def formatTime(seconds, total=None, short=False):
    """
    Format ``seconds`` (number of seconds) as a string representation.
    When ``short`` is False (the default) the format is:

        HH:MM:SS.

    Otherwise, the format is exacly 6 characters long and of the form:

        1w 3d
        2d 4h
        1h 5m
        1m 4s
        15s

    If ``total`` is not None it will also be formatted and
    appended to the result seperated by ' / '.
    """

    def time_tuple(ts):
        if ts is None or ts < 0:
            ts = 0
        hours = ts / 3600
        mins = ts % 3600 / 60
        secs = ts % 3600 % 60
        tstr = '%02d:%02d' % (mins, secs)
        if int(hours):
            tstr = '%02d:%s' % (hours, tstr)
        return (
         int(hours), int(mins), int(secs), tstr)

    if not short:
        hours, mins, secs, curr_str = time_tuple(seconds)
        retval = curr_str
        if total:
            hours, mins, secs, total_str = time_tuple(total)
            retval += ' / %s' % total_str
        return retval
    else:
        units = [
         ('y', 31449600),
         ('w', 604800),
         ('d', 86400),
         ('h', 3600),
         ('m', 60),
         ('s', 1)]
        seconds = int(seconds)
        if seconds < 60:
            return '   {0:02d}s'.format(seconds)
        for i in range(len(units) - 1):
            unit1, limit1 = units[i]
            unit2, limit2 = units[(i + 1)]
            if seconds >= limit1:
                return '{0:02d}{1}{2:02d}{3}'.format(seconds // limit1, unit1, seconds % limit1 // limit2, unit2)

        return '  ~inf'


def xpathFilter(xpaths):
    """
    FIXME
    """
    if isinstance(xpaths, str):
        xpaths = [(xpaths, None)]
    else:
        if isinstance(xpaths, tuple):
            if isinstance(xpaths[0], str):
                xpaths = [
                 xpaths]

    def wrapper(func):

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            from .stanzas import Stanza
            stanza = None
            for a in args:
                if isinstance(a, Stanza):
                    stanza = a
                    break

            if stanza is None:
                raise TypeError('No arguments of type Stanza found')
            for xp in xpaths:
                if isinstance(xp, str):
                    xp, ns_map = xp, None
                else:
                    xp, ns_map = xp
                if stanza.xml.xpath(xp, namespaces=ns_map):
                    return func(*args, **kwargs)

            async def _noOpCoro(*args, **kwargs):
                pass

            return _noOpCoro(*args, **kwargs)

        return wrapped_func

    return wrapper


_dns_cache = {}

async def resolveHostPort(hostname, port, loop, use_cache=True, client_srv=True, srv_records=None, srv_lookup=True):
    global _dns_cache

    def _chooseSrv(_srvs):
        return random.choice(_srvs)

    if use_cache and hostname in _dns_cache:
        cached = _dns_cache[hostname]
        if type(cached) is list:
            srv_choice = _chooseSrv(cached)
            resolved_srv = await resolveHostPort((srv_choice.host), (srv_choice.port),
              loop, use_cache=True,
              client_srv=client_srv,
              srv_lookup=False)
            return resolved_srv
        return cached
    else:
        resolver = aiodns.DNSResolver(loop=loop)
        ip = None
        try:
            ip = ip_address(hostname)
            return (str(ip), port)
        except ValueError:
            pass

        srv_query_type = '_xmpp-client' if client_srv else '_xmpp-server'
        try:
            srv = await resolver.query('{}._tcp.{}'.format(srv_query_type, hostname), 'SRV')
            srv_results = sorted(srv, key=(attrgetter('priority', 'weight')))
            if srv_records is not None:
                srv_records += srv_results
            _dns_cache[hostname] = srv_results
            srv_choice = _chooseSrv(srv_results)
            if srv_choice.host != hostname:
                resolved_srv = await resolveHostPort((srv_choice.host), (srv_choice.port),
                  loop, use_cache=use_cache,
                  client_srv=client_srv,
                  srv_lookup=False)
                _dns_cache[hostname] = resolved_srv
                return resolved_srv
        except aiodns.error.DNSError:
            pass

        arecord = await resolver.query(hostname, 'A')
        ip = arecord.pop()
        _dns_cache[hostname] = (ip, port)
        return (ip, port)