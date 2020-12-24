# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sphinxcontrib/smblink_test.py
# Compiled at: 2013-03-31 06:20:32
import smblink, unittest
unittestVerbosity = 0
verboseMode = False

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        if verboseMode:
            print '\n'

    def test_convertToWSLStyle_simpleStr(self):
        chkList = [['\\\\', '//'],
         [
          '\\\\path', '//path'],
         [
          '\\\\hoge\\new\\to\\path', '//hoge/new/to/path'],
         [
          '\\\\hoge\\space space\\to\\path', '//hoge/space%20space/to/path'],
         [
          '\\\\hoge\\^~{}[];@\\=&$# \\to\\path', '//hoge/%5E%7E%7B%7D%5B%5D%3B%40/%3D%26%24%23%20/to/path'],
         [
          '\\\\hoge\\\\%=%&$# \\to\\path', '//hoge//%25%3D%25%26%24%23%20/to/path']]
        for chk in chkList:
            self.assertEqual(chk[1], smblink.convertToWSLStyle(chk[0]))
            if verboseMode:
                print ' Input  : ' + chk[0] + '\n Assert : ' + chk[1] + '\n ---- '

    def test_convertToWSLStyle_multibyteStr(self):
        chkList = [
         [
          '\\\\日本語ほげほげ', '//日本語ほげほげ'],
         [
          '\\\\日本語ほげほげ\\日本語ふがふが', '//日本語ほげほげ/日本語ふがふが'],
         [
          '\\\\日本語^~{}[];@ほげほげ\\日本語=&$# ふがふが', '//日本語%5E%7E%7B%7D%5B%5D%3B%40ほげほげ/日本語%3D%26%24%23%20ふがふが']]
        for chk in chkList:
            self.assertEqual(chk[1], smblink.convertToWSLStyle(chk[0]))
            if verboseMode:
                print ' Input  : ' + chk[0] + '\n Assert : ' + chk[1] + '\n ---- '

    def test_smblink_role(self):
        chkList = [
         [
          ':smblink:`\\\\path`', '<a href="file://path">\\\\path</a>'],
         [
          ':smblink:`\\\\日本語ほげほげ`', '<a href="file://日本語ほげほげ">\\\\日本語ほげほげ</a>'],
         [
          '`\\\\path`', '<a href="file://path">\\\\path</a>'],
         [
          '\\\\path`', '<a href="file:"></a>'],
         [
          '`\\\\path', '<a href="file://path">\\\\path</a>'],
         [
          '\\\\path', '<a href="file://path">\\\\path</a>'],
         [
          ':smblink: `hoge <\\\\path>`', '<a href="file://path">hoge</a>'],
         [
          ':smblink: `hoge<\\\\path>`', '<a href="file://path">hoge</a>'],
         [
          ':smblink: `hoge        <\\\\path>    `', '<a href="file://path">hoge</a>']]
        for chk in chkList:
            self.assertEqual(chk[1], smblink.smblink_role('smblink', chk[0], '', '', '', '')[0][0].astext())
            if verboseMode:
                print ' Input  : ' + chk[0] + '\n Assert : ' + chk[1] + '\n ---- '


if __name__ == '__main__':
    unittest.main(verbosity=unittestVerbosity)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSequenceFunctions))
    return suite