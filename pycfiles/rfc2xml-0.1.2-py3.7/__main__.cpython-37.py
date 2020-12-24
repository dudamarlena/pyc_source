# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/__main__.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 737 bytes
from lxml import etree
import sys
from . import Rfc2Xml

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    filename = sys.argv[1]
    suppress_result = False
    for arg in sys.argv[2:]:
        if arg == '--suppress-result':
            suppress_result = True
        else:
            print('Unknown argument', arg)
            usage()
            sys.exit(2)

    with open(filename) as (fp):
        contents = fp.read()
    result = Rfc2Xml.parse(contents).to_xml()
    if not suppress_result:
        print(etree.tostring(result, pretty_print=True).decode())


def usage():
    print('Usage: python -m rfc2xml <filename> [--suppress-result]', file=(sys.stderr))


if __name__ == '__main__':
    main()