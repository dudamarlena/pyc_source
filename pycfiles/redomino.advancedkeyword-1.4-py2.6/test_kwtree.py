# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/tests/test_kwtree.py
# Compiled at: 2013-05-08 04:41:18
from redomino.advancedkeyword.tests.base import TestCase

class TestTreeKeywords(TestCase):
    """ Check if the tree keywords works fine
    """

    def _getTreeBrowserView(self, all_kw, selecteded_kw):
        from redomino.advancedkeyword.browser.keywords import KWGenerator

        class MockKeywordsKW(KWGenerator):

            def get_all_kw(self):
                return all_kw

            def get_selected_kw(self):
                return selecteded_kw

        return MockKeywordsKW(self.portal, self.portal.REQUEST)

    def test_keywords1(self):
        """ 
            Just one subject selected:

                * redomino

            Output structure:

                * redomino
        """
        l = [
         'redomino']
        data = self._getTreeBrowserView(l, l)()
        self.assertEquals(len(data), 1)
        self.assertFalse(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'redomino')
        self.assertEquals(data[0]['keyword'], 'redomino')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(data[0]['children'], [])

    def test_keywords2(self):
        """ 
            Two subjects selected:

                * redomino
                * redomino.prova.qualcosa

            Output:
 
               * redomino (selecteded)
               * redomino.prova (selecteded)
               * redomino.prova.qualcosa (selecteded)
        """
        l = [
         'redomino', 'redomino.prova.qualcosa']
        data = self._getTreeBrowserView(l, l)()
        self.assertEquals(len(data), 1)
        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'redomino')
        self.assertEquals(data[0]['keyword'], 'redomino')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 1)
        self.assertTrue(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[0]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[0]['children'][0]['selected'], True)
        self.assertEquals(len(data[0]['children'][0]['children']), 1)
        self.assertFalse(data[0]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[0]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[0]['children'][0]['children'][0]['selected'], True)
        self.assertEquals(data[0]['children'][0]['children'][0]['children'], [])

    def test_keywords3(self):
        """ 
            It's just one subject (an entire branch):

                * redomino.prova.qualcosa

            Output:
 
               * redomino (selecteded)
               * redomino.prova (selecteded)
               * redomino.prova.qualcosa (selecteded)
        """
        l = [
         'redomino.prova.qualcosa']
        data = self._getTreeBrowserView(l, l)()
        self.assertEquals(len(data), 1)
        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'redomino')
        self.assertEquals(data[0]['keyword'], 'redomino')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 1)
        self.assertTrue(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[0]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[0]['children'][0]['selected'], True)
        self.assertEquals(len(data[0]['children'][0]['children']), 1)
        self.assertFalse(data[0]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[0]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[0]['children'][0]['children'][0]['selected'], True)
        self.assertEquals(data[0]['children'][0]['children'][0]['children'], [])

    def test_keywords4(self):
        """ 
            Subjects:
            
            * pippo
            * redomino
            * redomino.prova.qualcosa

            Output (all tree nodes selecteded):

            * pippo
            * redomino
            * redomino.prova
            * redomino.prova.qualcosa
        """
        l = [
         'redomino', 'redomino.prova.qualcosa', 'pippo']
        data = self._getTreeBrowserView(l, l)()
        self.assertEquals(len(data), 2)
        self.assertFalse(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'pippo')
        self.assertEquals(data[0]['keyword'], 'pippo')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(data[0]['children'], [])
        self.assertTrue(data[1]['is_folder'])
        self.assertEquals(data[1]['full_keyword'], 'redomino')
        self.assertEquals(data[1]['keyword'], 'redomino')
        self.assertEquals(data[1]['selected'], True)
        self.assertEquals(len(data[1]['children']), 1)
        self.assertTrue(data[1]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[1]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[1]['children'][0]['selected'], True)
        self.assertEquals(len(data[1]['children'][0]['children']), 1)
        self.assertFalse(data[1]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['selected'], True)
        self.assertEquals(data[1]['children'][0]['children'][0]['children'], [])

    def test_keywords5(self):
        """ 
            All Subjects:
            
            * redomino
            * redomino.prova.qualcosa
            * pippo
            * pippo.pluto

            case 1 selected:
            
            * redomino
            * redomino.prova.qualcosa
            * pippo

            case 2 selected:
            
            * pippo.pluto

            Output for case 1:

            * redomino (selecteded)
            * pippo (selecteded)
            * pippo.pluto (UNselectedED)
            * redomino.prova (selecteded)
            * redomino.prova.qualcosa (selecteded)

            Output for case 2:

            * redomino (UNselectedED)
            * pippo (selecteded)
            * pippo.pluto (selecteded)
            * redomino.prova (UNselectedED)
            * redomino.prova.qualcosa (UNselectedED)
        """
        l = [
         'redomino.prova.qualcosa', 'pippo', 'pippo.pluto']
        l2 = ['redomino.prova.qualcosa', 'pippo']
        l3 = ['pippo.pluto']
        data = self._getTreeBrowserView(l, l2)()
        self.assertEquals(len(data), 2)
        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'pippo')
        self.assertEquals(data[0]['keyword'], 'pippo')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 1)
        self.assertFalse(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'pippo.pluto')
        self.assertEquals(data[0]['children'][0]['keyword'], 'pluto')
        self.assertEquals(data[0]['children'][0]['selected'], False)
        self.assertEquals(data[0]['children'][0]['children'], [])
        self.assertTrue(data[1]['is_folder'])
        self.assertEquals(data[1]['full_keyword'], 'redomino')
        self.assertEquals(data[1]['keyword'], 'redomino')
        self.assertEquals(data[1]['selected'], True)
        self.assertEquals(len(data[1]['children']), 1)
        self.assertTrue(data[1]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[1]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[1]['children'][0]['selected'], True)
        self.assertEquals(len(data[1]['children'][0]['children']), 1)
        self.assertFalse(data[1]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['selected'], True)
        self.assertEquals(data[1]['children'][0]['children'][0]['children'], [])
        data = self._getTreeBrowserView(l, l3)()
        self.assertEquals(len(data), 2)
        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'pippo')
        self.assertEquals(data[0]['keyword'], 'pippo')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 1)
        self.assertFalse(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'pippo.pluto')
        self.assertEquals(data[0]['children'][0]['keyword'], 'pluto')
        self.assertEquals(data[0]['children'][0]['selected'], True)
        self.assertEquals(data[0]['children'][0]['children'], [])
        self.assertTrue(data[1]['is_folder'])
        self.assertEquals(data[1]['full_keyword'], 'redomino')
        self.assertEquals(data[1]['keyword'], 'redomino')
        self.assertEquals(data[1]['selected'], False)
        self.assertEquals(len(data[1]['children']), 1)
        self.assertTrue(data[1]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[1]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[1]['children'][0]['selected'], False)
        self.assertEquals(len(data[1]['children'][0]['children']), 1)
        self.assertFalse(data[1]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['selected'], False)
        self.assertEquals(data[1]['children'][0]['children'][0]['children'], [])

    def test_keywords6(self):
        """ 
            Subjects:

            * redomino
            * redomino.test
            * redomino.test test2

            selected:
            
            * redomino.test

            Output:

            * redomino
            * redomino.test
        """
        l = [
         'redomino', 'redomino.test', 'redomino.test test2']
        l2 = ['redomino.test']
        data = self._getTreeBrowserView(l, l2)()
        self.assertEquals(len(data), 1)
        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'redomino')
        self.assertEquals(data[0]['keyword'], 'redomino')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 2)
        self.assertFalse(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'redomino.test')
        self.assertEquals(data[0]['children'][0]['keyword'], 'test')
        self.assertEquals(data[0]['children'][0]['selected'], True)
        self.assertFalse(data[0]['children'][1]['is_folder'])
        self.assertEquals(data[0]['children'][1]['full_keyword'], 'redomino.test test2')
        self.assertEquals(data[0]['children'][1]['keyword'], 'test test2')
        self.assertEquals(data[0]['children'][1]['selected'], False)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTreeKeywords))
    return suite