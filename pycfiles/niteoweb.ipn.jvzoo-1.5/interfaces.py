# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.jvzoo/src/niteoweb/ipn/jvzoo/interfaces.py
# Compiled at: 2013-10-02 09:19:46
"""Module where all interfaces, events and exceptions live."""
from niteoweb.ipn.jvzoo import JVZooMessageFactory as _
from zope import schema
from zope.interface import Interface

class IJVZooSettings(Interface):
    """Definition of fields for niteoweb.ipn.jvzoo configuration form."""
    secretkey = schema.Password(title=_('JVZoo Secret Key'), description=_('help_secretkey', default='Enter the Secret Key you got from JVZoo to access their API.'), required=True)


class JVZooError(Exception):
    """Base class for niteoweb.ipn.jvzoo exception."""
    pass


class SecretKeyNotSet(JVZooError):
    """Exception thrown when secret-key for @@jvzoo is not set."""
    pass


class UnknownTransactionType(JVZooError):
    """Exception through when Transaction Type is not known."""
    pass