# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mjjoyce/Coding/AIT/AIT-GUI/ait/gui/bin/ait_gui.py
# Compiled at: 2019-06-13 13:28:14
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