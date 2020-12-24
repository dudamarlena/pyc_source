# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fxg2svg/convert.py
# Compiled at: 2016-07-23 07:50:26
# Size of source mod 2**32: 1105 bytes
from lxml import etree
import logging, sys, argparse
from . import fxg2svg
LOGLEVELMAP = {'debug': logging.DEBUG, 
 'info': logging.INFO, 
 'warning': logging.WARNING, 
 'error': logging.ERROR}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('fxg', help='fxg file')
    parser.add_argument('-l', '--log-level', choices=LOGLEVELMAP.keys(), default='info', help='set log level')
    parser.add_argument('-o', '--output', help='output svg filename')
    parser.add_argument('-f', '--fontdir', help='directory to fonts')
    args = parser.parse_args()
    fxg_bytes = open(args.fxg, 'r')
    logging.basicConfig(format='%(levelname)-6s| %(message)s', level=LOGLEVELMAP[args.log_level])
    if args.output is not None:
        svg = args.output
    else:
        svg = '%s.svg' % '.'.join(args.fxg.split('.')[:-1])
    fxg2svg(fxg_bytes, args.fontdir).getroottree().write(svg, encoding='UTF-8', xml_declaration=True)


if __name__ == '__main__':
    main()