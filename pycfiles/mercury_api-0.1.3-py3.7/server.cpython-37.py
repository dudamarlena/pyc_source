# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_api/server.py
# Compiled at: 2018-08-21 12:33:14
# Size of source mod 2**32: 1416 bytes
import logging
from gevent.pywsgi import WSGIServer
from mercury_api.configuration import get_api_configuration
import mercury_api.app as app
log = logging.getLogger(__name__)

def main():
    """
    Gevent WSGI server launcher with graceful stop.
    """
    config = get_api_configuration()
    logging.basicConfig(level=(logging.getLevelName(config.logging.level)),
      format=(config.logging.format))
    http_server = WSGIServer((config.api.host, config.api.port), app)
    try:
        log.info('Starting gevent WSGI service')
        log.debug(config)
        http_server.serve_forever()
    except KeyboardInterrupt:
        log.info('Stopping gevent WSGI service')
        http_server.stop()


if __name__ == '__main__':
    main()