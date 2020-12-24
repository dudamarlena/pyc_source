# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/canoe/main.py
# Compiled at: 2013-03-20 10:50:18
from optparse import OptionParser
from config import Config
from watch import start_watch
parser = OptionParser()
parser.add_option('-c', '--config', default='', dest='config', help='path to config file')

def main():
    options, args = parser.parse_args()
    conf = Config.from_file(options.config)
    if not conf:
        raise SystemExit()
    start_watch(conf)