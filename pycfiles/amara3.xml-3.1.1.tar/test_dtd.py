# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/beazley/Projects/amara/test/xmlcore/test_dtd.py
# Compiled at: 2010-03-01 11:56:29
import unittest
from cStringIO import StringIO
from amara import parse
from amara.lib import treecompare
from amara.test import file_finder
ATOMENTRY1 = '<?xml version="1.0" encoding="UTF-8"?>\n<entry xmlns=\'http://www.w3.org/2005/Atom\'><id>urn:bogus:x</id><title>boo</title></entry>'
XMLDECL = '<?xml version="1.0" encoding="UTF-8"?>\n'
FILE = file_finder(__file__)

def test_parse_with_dtd():
    TEST_FILE = FILE('4suite.xsa')
    doc = parse(TEST_FILE, validate=True)


if __name__ == '__main__':
    raise SystemExit('use nosetests')