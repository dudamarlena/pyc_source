# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testPegasusHdr.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for pegasus/kickstart_hdr.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testPegasusHdr.py 23596 2009-03-18 03:58:50Z dang $'
import unittest
from netlogger.tests import shared
import time, tempfile
from netlogger.pegasus.kickstart_hdr import *

class TestCase(shared.BaseTestCase):
    """Unit test cases for the jobstate_hdr module.
    """

    def testHeader(self):
        """Add header line to a file and verify it.
        """
        orig_line = 'This is the original text of the file.\n'
        tmp = tempfile.NamedTemporaryFile()
        filename = tmp.name
        file(filename, 'w').write(orig_line)
        header_line = 'Header text and a newline\n'
        addHeader(filename, header_line)
        f = file(filename)
        line = f.readline()
        assert line == header_line
        line = f.readline()
        assert line == orig_line

    def testLabel(self):
        """Add a label to a file and read it back.
        """
        value = 'xyz'
        temp_file = tempfile.NamedTemporaryFile()
        attr = WorkflowLabelHandler.ATTR
        temp_file.write('<?xml version="1.0"?>\n')
        temp_file.write('<invocation foo="Bar" %s="%s" >\n' % (attr, value))
        temp_file.write('</invocation>\n')
        temp_file.seek(0)
        filename, expected = temp_file.name, value
        label = getWorkflowLabel(file(filename))
        self.debug_('LABEL: %s' % label)
        self.assertEqual(label, expected)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()