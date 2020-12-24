# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testIncConfigObj.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for util.IncConfigObj class
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testIncConfigObj.py 23596 2009-03-18 03:58:50Z dang $'
from netlogger import configobj
import tempfile, unittest
from netlogger.tests import shared
from netlogger.util import IncConfigObj

class TestCase(shared.BaseTestCase):
    """Unit test cases.
    """

    def setUp(self):
        self.debug_('create files')
        self.files = [ tempfile.NamedTemporaryFile() for i in range(4) ]
        self.files[0].write('# main file\n @include %s\n[hello]\nmessage = "hello, $name"\n@include %s\n@include %s\n' % (
         self.files[1].name, self.files[2].name,
         self.files[3].name))
        self.files[1].write('name = Dan\n')
        self.files[2].write('[goodbye]\nmessage = "goodbye, $name"\n')
        self.files[3].write('[sayonara]\nmessage = "sayonara, $name"\n')
        map(lambda f: f.seek(0), self.files)
        self.debug_('main file: %s' % self.files[0].name)
        self.debug_('included files: %s' % (',').join([ n.name for n in self.files[1:] ]))

    def testInclude(self):
        """Test IncConfigObj @include directive
        """
        self.debug_("configure from file '%s'" % self.files[0].name)
        obj = IncConfigObj(self.files[0].name, interpolation='Template', file_error='True')
        for salut in ('hello', 'goodbye', 'sayonara'):
            self.assert_(obj[salut]['message'] == '%s, Dan' % salut)

    def testIncludeErr(self):
        """Test error reporting for @include
        """
        self.files[1].seek(0, 2)
        self.files[1].write('- bad -\n')
        self.files[1].flush()
        try:
            self.debug_("configure from file '%s'" % self.files[0].name)
            obj = IncConfigObj(self.files[0].name, interpolation='Template', file_error='True')
        except configobj.ConfigObjError, E:
            msg = str(E)
            missing = self.files[1].name
            self.assert_(msg.find(missing) > 0, "couldn't find '%s' in error message" % missing)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()