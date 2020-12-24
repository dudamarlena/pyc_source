# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/termine/genericargparse.py
# Compiled at: 2012-07-12 16:35:39
from termine.gwise import Groupwise, CONFIGFILE, initialConfig
from termine.gwexceptions import *
import ConfigParser, os
try:
    import argparse
except ImportError:
    raise GWFatalException, 'For Python < 2.7 you need to install argparse'

config = ConfigParser.SafeConfigParser()
if not os.path.isfile(CONFIGFILE):
    initialConfig(CONFIGFILE)
config.read(CONFIGFILE)
DEFAULT_FMT = config.get('Global', 'DEFAULT_FMT')
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--verbose', '-v', action='count')
parser.add_argument('--version', action='version', version='%(prog)s 1')
parser.add_argument('--format', '-f', dest='format', default=DEFAULT_FMT)
parser.add_argument('--force-login', dest='forcelogin', action='store_true', default=False)