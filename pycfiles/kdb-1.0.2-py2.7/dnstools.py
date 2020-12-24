# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugins/dnstools.py
# Compiled at: 2014-04-26 09:00:59
"""DNS Tools

This plugin provides various tools to work with
hostnames and ip addresses.
"""
__version__ = '0.0.4'
__author__ = 'James Mills, prologic at shortcircuit dot net dot au'
from traceback import format_exc
from socket import gethostbyaddr, gethostbyname
from circuits import Component
from funcy import first
from ..utils import log
from ..plugin import BasePlugin

class Commands(Component):
    channel = 'commands'

    def resolve(self, source, target, args):
        """Synonym, of HOST

        See: HOST
        """
        return self.host(source, target, args)

    def host(self, source, target, args):
        """Resolve a hostname or ip address.

        Syntax: HOST [<hostname>] | [<ip>]
        """
        if not args:
            return 'No hostname or ip address specified.'
        tokens = args.split(' ', 1)
        host = first(tokens)
        isip = all(c.isdigit() for c in host.replace('.', ''))
        if isip:
            try:
                name, aliases, addresses = gethostbyaddr(host)
                msg = ('{0:s} -> {1:s}').format(host, name)
            except Exception as error:
                msg = log('ERROR: {0:s}', error)
                log(format_exc())

        else:
            try:
                address = gethostbyname(host)
                msg = ('{0:s} -> {1:s}').format(host, address)
            except Exception as error:
                msg = log('ERROR: {0:s}', error)
                log(format_exc())

        return msg


class DNSTools(BasePlugin):
    """DNS Tools Plugin

    Provides commands for working with DNS (Domain Name Servers).
    See: commands dnstools
    """

    def init(self, *args, **kwargs):
        super(DNSTools, self).init(*args, **kwargs)
        Commands().register(self)