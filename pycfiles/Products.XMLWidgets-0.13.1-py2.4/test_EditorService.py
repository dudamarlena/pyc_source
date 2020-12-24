# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/Products/XMLWidgets/tests/test_EditorService.py
# Compiled at: 2008-08-28 08:23:26
import unittest
try:
    import Zope2
except ImportError:
    import Zope as Zope2

try:
    import transaction
except ImportError:

    class TransactionMan:
        __module__ = __name__

        def begin(self):
            get_transaction().begin()

        def commit(self, sub=False):
            get_transaction().commit(sub)

        def abort(self, sub=False):
            get_transaction().abort(sub)

        def get(self):
            return get_transaction()


    transaction = TransactionMan()

from Products.ParsedXML.ParsedXML import ParsedXML
xml = '<?xml version="1.0" ?>\n<doc><p>A paragraph</p><p>Paragraph two, the sequel.</p><section><p>Sub p</p><section><p>Sub sub</p></section></section></doc>\n'

class FakeRequest:
    __module__ = __name__

    def __init__(self):
        self.SESSION = {}
        self.dict = {'SERVER_URL': 'this_server'}
        self._script = ['script']

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, object):
        self.dict[key] = object

    def get(self, key, default):
        return self.dict.get(key, default)


class EditorServiceTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        transaction.begin()
        self.connection = Zope2.DB.open()
        self.root = root = self.connection.root()['Application']
        root.manage_addProduct['ParsedXML'].manage_addParsedXML('doc1', file=xml)
        root.manage_addProduct['ParsedXML'].manage_addParsedXML('doc2', file=xml)
        root.REQUEST = FakeRequest()
        self.doc1 = root.doc1
        self.doc2 = root.doc2
        root.manage_addProduct['XMLWidgets'].manage_addEditorService('service_editor')
        self.s = root.service_editor
        root.manage_addFolder('alpha')
        alpha = root.alpha
        alpha.manage_addFolder('doc')
        alpha.manage_addFolder('p')
        alpha.manage_addFolder('section')
        root.manage_addFolder('beta')
        beta = root.beta
        beta.manage_addFolder('doc')
        beta.manage_addFolder('section')
        beta.manage_addFolder('p')
        beta.manage_addFolder('section_focus')
        beta.manage_addFolder('p_focus')
        root.manage_addFolder('gamma')
        gamma = root.gamma
        gamma.manage_addFolder('section')
        gamma.manage_addFolder('p')
        gamma.manage_addFolder('section_focus')
        gamma.manage_addFolder('p_focus')
        root.manage_addProduct['XMLWidgets'].manage_addWidgetRegistry('wr1')
        self.wr1 = root.wr1
        root.manage_addProduct['XMLWidgets'].manage_addWidgetRegistry('wr2')
        self.wr2 = root.wr2
        root.manage_addProduct['XMLWidgets'].manage_addWidgetRegistry('wr3')
        self.wr3 = root.wr3
        self.wr1.addWidget('doc', ('alpha', 'doc'))
        self.wr1.addWidget('p', ('alpha', 'p'))
        self.wr1.addWidget('section', ('alpha', 'section'))
        self.wr2.addWidget('doc', ('beta', 'doc'))
        self.wr2.addWidget('section', ('beta', 'section'))
        self.wr2.addWidget('p', ('beta', 'p'))
        self.wr3.addWidget('section', ('gamma', 'section'))
        self.wr3.addWidget('p', ('gamma', 'p'))

    def tearDown(self):
        transaction.abort()
        self.connection.close()

    def test_DocumentEditor(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        self.assertEquals(('alpha', 'doc'), self.s._getWidgetPath(self.doc1.documentElement))
        self.assertEquals(self.root.alpha.doc, self.s.getWidget(self.doc1.documentElement))
        node = self.doc1.documentElement.childNodes[0]
        self.assertEquals(self.root.alpha.p, self.s.getWidget(node))
        node = self.doc1.documentElement.childNodes[2]
        self.assertEquals(self.root.alpha.section, self.s.getWidget(node))

    def test_DocumentEditor2(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        self.s.setDocumentEditor(self.doc2, 'wr2')
        self.assertEquals(self.root.alpha.doc, self.s.getWidget(self.doc1.documentElement))
        self.assertEquals(self.root.beta.doc, self.s.getWidget(self.doc2.documentElement))

    def test_Editor(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        self.s.setEditor(self.doc1.documentElement.childNodes[2], 'wr2')
        self.assertEquals(self.root.alpha.doc, self.s.getWidget(self.doc1.documentElement))
        self.assertEquals(self.root.alpha.p, self.s.getWidget(self.doc1.documentElement.childNodes[1]))
        self.assertEquals(self.root.beta.section, self.s.getWidget(self.doc1.documentElement.childNodes[2]))
        self.assertEquals(self.root.beta.p, self.s.getWidget(self.doc1.documentElement.childNodes[2].childNodes[0]))

    def test_NodeWidget(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        section_node = self.doc1.documentElement.childNodes[2]
        self.s.setNodeWidget(section_node, ('beta', 'section'))
        self.assertEquals(self.root.beta.section, self.s.getWidget(section_node))
        p_node = self.doc1.documentElement.childNodes[0]
        self.s.setNodeWidget(p_node, ('beta', 'p'))
        self.assertEquals(self.root.beta.p, self.s.getWidget(p_node))
        self.assertEquals(self.root.alpha.section, self.s.getWidget(section_node))

    def test_NodeWidget2(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        section_node = self.doc1.documentElement.childNodes[2]
        self.assertEquals(self.root.alpha.section, self.s.getWidget(section_node))
        self.s.setNodeWidget(section_node, ('beta', 'section'))
        self.assertEquals(self.root.beta.section, self.s.getWidget(section_node))
        self.s.clearNodeWidget(self.doc1.documentElement)
        self.assertEquals(self.root.alpha.section, self.s.getWidget(section_node))

    def test_EditorNodeWidget(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        section_node = self.doc1.documentElement.childNodes[2]
        self.s.setNodeWidget(section_node, ('beta', 'section'))
        self.assertEquals(self.root.beta.section, self.s.getWidget(section_node))
        p_node = self.doc1.documentElement.childNodes[0]
        self.s.setNodeWidget(p_node, ('beta', 'p'))
        self.assertEquals(self.root.beta.p, self.s.getWidget(p_node))
        self.assertEquals(self.root.alpha.section, self.s.getWidget(section_node))

    def test_EditorNodeWidget2(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        section_node = self.doc1.documentElement.childNodes[2]
        self.s.setNodeWidget(section_node, ('beta', 'section'))
        self.assertEquals(self.root.beta.section, self.s.getWidget(section_node))
        p_node = self.doc1.documentElement.childNodes[0]
        self.s.setNodeWidget(p_node, ('beta', 'p'))
        self.assertEquals(self.root.beta.p, self.s.getWidget(p_node))
        self.assertEquals(self.root.alpha.section, self.s.getWidget(section_node))

    def test_Root(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        section_node = self.doc1.documentElement.childNodes[2]
        self.s.pushRoot(section_node, 'wr2')
        self.assertEquals(self.root.beta.section, self.s.getWidget(section_node))
        self.s.popRoot(section_node)
        self.assertEquals(self.root.alpha.section, self.s.getWidget(section_node))

    def test_getNode(self):
        self.s.setDocumentEditor(self.doc1, 'wr1')
        p_node = self.doc1.documentElement.childNodes[0]
        section_node = self.doc1.documentElement.childNodes[2]
        doc_node = self.doc1.documentElement
        self.s.setNodeWidget(section_node, ('beta', 'section'))
        self.assertEquals(section_node, self.s.getNode(doc_node))
        self.s.setNodeWidget(p_node, ('beta', 'p'))
        self.assertEquals(p_node, self.s.getNode(doc_node))
        self.s.clearNodeWidget(p_node)
        self.assertEquals(None, self.s.getNode(doc_node))
        return


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EditorServiceTestCase, 'test'))
    return suite


def main():
    unittest.TextTestRunner().run(test_suite())


if __name__ == '__main__':
    main()