# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/phdoc/cli/parser.py
# Compiled at: 2013-09-24 11:14:47
import os, argparse, phdoc
from phdoc.config import Config
parser = argparse.ArgumentParser(**{'prog': 'phdoc', 
   'description': 'A lightweight Markdown-based wiki build tool.'})
parser.add_argument('-v', '--version', action='version', version=phdoc.__version__)
config = parser.add_argument('--config', '-c', default=os.getcwd(), help='Use the specified Markdoc config (a YAML file or a directory containing phdoc.yaml)')
log_level = parser.add_argument('--log-level', '-l', metavar='LEVEL', default='INFO', choices=('DEBUG INFO WARN ERROR').split(), help='Choose a log level from DEBUG, INFO (default), WARN or ERROR')
quiet = parser.add_argument('--quiet', '-q', action='store_const', dest='log_level', const='ERROR', help='Alias for --log-level ERROR')
verbose = parser.add_argument('--verbose', action='store_const', dest='log_level', const='DEBUG', help='Alias for --log-level DEBUG')
subparsers = parser.add_subparsers(dest='command', title='commands', metavar='COMMAND')