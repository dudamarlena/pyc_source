# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/lamson/handlers/forward.py
# Compiled at: 2011-05-21 19:39:14
"""
Implements a forwarding handler that will take anything it receives and
forwards it to the relay host.  It is intended to use with the
lamson.routing.RoutingBase.UNDELIVERABLE_QUEUE if you want mail that Lamson
doesn't understand to be delivered like normal.  The Router will dump
any mail that doesn't match into that queue if you set it, and then you can
load this handler into a special queue receiver to have it forwarded on.

BE VERY CAREFUL WITH THIS.  It should only be used in testing scenarios as
it can turn your server into an open relay if you're not careful.  You
are probably better off writing your own version of this that knows a list
of allowed hosts your machine answers to and only forwards those.
"""
from lamson.routing import route, stateless
from config import settings
import logging

@route('(to)@(host)', to='.+', host='.+')
@stateless
def START(message, to=None, host=None):
    """Forwards every mail it gets to the relay.  BE CAREFULE WITH THIS."""
    logging.debug('MESSAGE to %s@%s forwarded to the relay host.', to, host)
    settings.relay.deliver(message)