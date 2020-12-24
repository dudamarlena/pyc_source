# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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