# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/oofill/tests/test_1.py
# Compiled at: 2008-04-03 09:12:50
from unittest import TestCase, TestSuite, makeSuite
from oofill.parser import OOFill

def getAbsPathOfTestFile(name):
    from os.path import dirname, join
    return join(dirname(__file__), name)


class OOFillTests(TestCase):
    """
    Test suite for udp.
    """
    __module__ = __name__

    def test_OOFill_identity(self):

        class Test1View:
            __module__ = __name__

        a = file(getAbsPathOfTestFile('test1.odt'))
        ofilinst = OOFill(a)
        b = ofilinst.render(Test1View())

    def test_OOFill_insertblock(self):

        class Test1View:
            __module__ = __name__

            def titreOrdreDuJour(self):
                import time
                text = '<text:p  text:outline-level="2" text:style-name="P2">'
                text += 'Séance du %s' % time.ctime()
                text += '</text:p>'
                return text.decode('utf-8')

        a = file(getAbsPathOfTestFile('test1.odt'))
        ofilinst = OOFill(a)
        ofilinst.render(Test1View(), getAbsPathOfTestFile('test1_out.odt'))

    def test_OOFill_replaceblock(self):

        class Test2View:
            __module__ = __name__

            def replaceTitreOrdreDuJour(self):
                import time
                text = '<text:p  text:outline-level="2" text:style-name="P2">'
                text += 'Séance du %s' % time.ctime()
                text += '</text:p>'
                return text.decode('utf-8')

        a = file(getAbsPathOfTestFile('test2.odt'))
        ofilinst = OOFill(a)
        ofilinst.render(Test2View(), getAbsPathOfTestFile('test2_out.odt'))


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(OOFillTests))
    return suite


if __name__ == '__main__':
    framework()