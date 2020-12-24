# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/main.py
# Compiled at: 2018-01-04 04:15:46
# Size of source mod 2**32: 1148 bytes
import argparse, os
from cliez import conf
from cliez.parser import parse
from cabric import version
conf.COMPONENT_ROOT = os.path.dirname(__file__)
conf.GENERAL_ARGUMENTS = [
 (
  ('--dir', ),
  dict(nargs='?', default=os.getcwd(), help='set working directory')),
 (
  ('--debug', ), dict(action='store_true', help='open debug mode')),
 (
  ('--verbose', '-v'), dict(action='count')),
 (
  ('--env', '-s'), dict(nargs='?', default='beta', help='set environment')),
 (
  ('--hosts-file', ), dict(help='chose another hosts file to load'))]
conf.EPILOG = 'You can submit issues at: https://www.github.com/nextoa/cabric'

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=conf.EPILOG)
    for v in conf.GENERAL_ARGUMENTS:
        parser.add_argument(*v[0], **v[1])

    parser.add_argument('--version', '-V', action='version', version='%(prog)s v{}'.format(version))
    parse(parser)


if __name__ == '__main__':
    main()