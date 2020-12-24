# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/repoze/what/plugins/ip/ip_from.py
# Compiled at: 2010-06-24 15:26:07
from repoze.what.predicates import Predicate
from ipaddr import IPNetwork, IPv4Network, IPv6Network, IPAddress as IP
from types import ListType
import logging
log = logging.getLogger(__name__)

class ip_from(Predicate):
    """ Only allow access to specified IPs through specified proxies"""
    message = 'Access denied for this IP'

    def __init__(self, allowed=None, proxies=None, message=None, **kwargs):
        """
        @param allowed: the ip or list of ips allowed to access the wsgi server
        @param proxy: the ip or list of ips of permitted proxies to access the
                      wsgi server through
        @param message: The message to return when check fails
        """
        allowed = [allowed] if type(allowed) is not ListType else allowed
        self.message = message if message else self.message
        self.allowed = []
        for address in allowed:
            if address is None:
                continue
            ip = None
            try:
                ip = IP(address)
            except ValueError:
                try:
                    ip = IPNetwork(address)
                except ValueError:
                    pass

            if ip:
                self.allowed.append(ip)

        if isinstance(proxies, (str, unicode)):
            proxies = [proxies]
        if isinstance(proxies, (list, tuple)):
            self.proxies = []
            for address in proxies:
                if address is None:
                    continue
                ip = None
                try:
                    ip = IP(address)
                except ValueError:
                    try:
                        ip = IPNetwork(address)
                    except ValueError:
                        pass

                if ip:
                    self.proxies.append(ip)

        else:
            self.proxies = bool(proxies)
        super(ip_from, self).__init__(**kwargs)
        return

    def evaluate(self, environ, credentials):
        """
        check that the request ip and proxy are in the allowed lists
        @return: Boolean
        """
        remote_str = environ.get('REMOTE_ADDR')
        if remote_str:
            try:
                remote = IP(remote_str)
            except ValueError:
                self.unmet()

        if not remote_str or not remote:
            self.unmet()
        forwarded_str = environ.get('HTTP_X_FORWARDED_FOR')
        if forwarded_str:
            proxy = remote
            proxy_str = remote_str
            remote_str = forwarded_str
            try:
                remote = IP(remote_str)
            except ValueError:
                self.unmet()
            else:
                if not remote:
                    self.unmet()
        else:
            proxy = proxy_str = None
        msg = 'Remote IP: %s Attempting Access' % remote
        if proxy:
            msg += ' Through %s' % proxy
        log.debug(msg)
        if proxy:
            if isinstance(self.proxies, (list, tuple)):
                valid = False
                for address in self.proxies:
                    if isinstance(address, (IPv4Network, IPv6Network)) and proxy in address or proxy == address:
                        log.debug('Proxy Validated')
                        valid = True
                        break

                if not valid:
                    log.warn('Failed Access Attempt by %s through %s' % (
                     remote_str, proxy_str))
                    self.unmet('Access denied through this proxy')
            elif not self.proxies:
                self.unmet('Access through proxies denied')
        valid = False
        for address in self.allowed:
            if isinstance(address, (IPv4Network, IPv6Network)) and remote in address or remote == address:
                log.debug('IP Validated')
                valid = True
                break

        if valid:
            identity = environ.get('repoze.who.identity')
            if not identity:
                identity = {}
                environ['repoze.who.identity'] = identity
            identity['ip'] = remote.compressed
            if proxy:
                identity['proxy'] = proxy.compressed
        else:
            msg = 'Failed Access Attempt by %s' % remote_str
            if proxy_str is not None:
                msg += ' Through %s' % proxy_str
            log.warn(msg)
            self.unmet(self.message)
        return