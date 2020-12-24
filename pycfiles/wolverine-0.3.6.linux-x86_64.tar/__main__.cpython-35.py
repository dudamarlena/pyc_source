# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lance/.virtualenvs/wolverine/lib/python3.5/site-packages/wolverine/web/__main__.py
# Compiled at: 2015-10-30 12:46:20
# Size of source mod 2**32: 1077 bytes
import asyncio, logging
from optparse import OptionParser
import os
from wolverine import MicroApp
from wolverine.gateway import GatewayModule
from wolverine.web import WebModule
LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s'

def web():
    log_level = logging.INFO
    usage = 'usage: %prog [options] arg'
    parser = OptionParser(usage)
    parser.add_option('-l', '--log-level', dest='log_level', help='log level one of (DEBUG, INFO, WARNING, ERROR, Critical)', default='ERROR')
    options, args = parser.parse_args()
    if options.log_level:
        log_level = getattr(logging, options.log_level.upper())
    logging.basicConfig(level=log_level, format=LOG_FORMAT)
    loop = asyncio.get_event_loop()
    app = MicroApp(loop=loop)
    gateway = GatewayModule()
    app.register_module(gateway)
    web_console = WebModule()
    app.register_module(web_console)
    app.run()


if __name__ == '__main__':
    web()