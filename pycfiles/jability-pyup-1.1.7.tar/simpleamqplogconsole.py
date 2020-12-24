# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/simpleamqplogconsole.py
# Compiled at: 2013-05-25 04:38:30
from amqp.logconsole import LogConsole
from configJSON import ConfigJSON
from toolbox import printu
import sys, os.path
if __name__ == '__main__':
    if os.path.exists(sys.argv[1]):
        filename = sys.argv[1]
    else:
        filename = os.path.join(os.path.dirname(__file__), 'simpleamqplogconsole.conf.json')
    cfgfile = ConfigJSON(filename)
    if cfgfile.exists():
        conf = cfgfile.load()
        logconsole = LogConsole(conf)
        logconsole.run()
    else:
        printu('Cannot read configuration file "%s"' % filename)