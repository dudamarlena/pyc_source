# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/apiscrub/main.py
# Compiled at: 2018-10-09 16:30:56
# Size of source mod 2**32: 1302 bytes
__doc__ = '\nScrubs an OpenAPI file for distribution.\n\nUsage:\nscrub --keep admin channels/openapi.yaml channels/admin.yaml\n\nResources in the OpenAPI file are marked with a string or list of tags. This\nalso works for examples!\n\n- name: param1\n  x-only: admin\n'
import argparse, sys
from ruamel.yaml import YAML
from apiscrub import process

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='Source OpenAPI document')
    parser.add_argument('destination',
      help='Destination for rendered OpenAPI output')
    parser.add_argument('-t', '--tag', default='x-only', help='Object property tag name to check')
    parser.add_argument('-k', '--keep', default='', help='Names to keep in the output')
    args = parser.parse_args()
    yaml = YAML()
    if args.source == '-':
        src = sys.stdin
    else:
        src = open(args.source)
    doc = yaml.load(src)
    process(args.tag, set(args.keep.split(',')), doc)
    if args.destination == '-':
        dest = sys.stdout
    else:
        dest = open(args.destination, 'w')
    yaml.dump(doc, dest)


if __name__ == '__main__':
    run()