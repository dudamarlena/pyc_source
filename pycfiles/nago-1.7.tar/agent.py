# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/nago/nago/extensions/agent.py
# Compiled at: 2014-01-22 14:21:09
""" Manage settings on a local node """
__requires__ = [
 'jinja2 >= 2.4']
import pkg_resources, nago.core
from nago.core import nago_access
import nago.protocols.httpserver, unittest

@nago_access()
def start(debug=False, host='127.0.0.1'):
    """ starts a nago agent (daemon) process """
    if debug:
        debug = True
    nago.protocols.httpserver.app.run(debug=debug, host=host)


@nago_access()
def stop(key, section='main'):
    """ stops the nago agent
    """
    pass