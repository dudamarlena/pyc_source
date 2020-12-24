# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/awaldron/Projects/ait/ait-gui/ait/gui/bin/ait_gui.py
# Compiled at: 2018-11-28 19:09:32
import argparse, socket, sys, gevent, gevent.monkey, geventwebsocket
gevent.monkey.patch_all()
import ait.core, ait.gui
try:
    ait.core.log.begin()
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', dest='browser', default='none')
    parser.add_argument('--host', dest='host')
    parser.add_argument('port', nargs='?', type=int, default=ait.config.get('gui.port', 8080))
    arguments = parser.parse_args()
    browser = arguments.browser
    host = arguments.host
    port = arguments.port
    if host is None:
        if sys.platform == 'darwin':
            host = 'localhost'
        else:
            host = socket.gethostname().split('.')[0]
    url = 'http://%s:%d' % (host, port)
    ait.gui.init(host, port)
    ait.gui.startBrowser(url, browser)
    ait.core.log.info('Connect to %s' % url)
    ait.core.log.info('Ctrl-C to exit')
    ait.gui.wait()
except KeyboardInterrupt:
    ait.core.log.info('Received Ctrl-C.  Stopping AIT GUI.')
    ait.gui.cleanup()
except Exception as e:
    ait.core.log.error('AIT GUI error: %s' % str(e))

ait.core.log.end()