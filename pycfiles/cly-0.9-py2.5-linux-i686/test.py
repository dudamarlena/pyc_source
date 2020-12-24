# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cly/test.py
# Compiled at: 2007-12-09 06:21:11
import unittest, doctest
from cly import Grammar, Parser

class TestXMLGrammar(unittest.TestCase):
    """Test XML grammar parser."""

    def setUp(self):
        self._output = None
        return

    def _echo(self, **kwargs):
        self._output = kwargs

    def test_basic(self):
        xml = '<?xml version="1.0"?>\n        <grammar>\n            <node name=\'echo\'>\n                <variable name=\'text\'>\n                    <action callback=\'echo\'/>\n                </variable>\n            </node>\n        </grammar>\n        '
        grammar = Grammar.from_xml(xml, echo=self._echo)
        parser = Parser(grammar)
        parser.execute('echo magic')
        self.assertEqual(self._output, {'text': 'magic'})

    def test_integer_types(self):
        xml = '<?xml version="1.0"?>\n        <grammar>\n            <node name=\'echo\'>\n                <variable name=\'text\' traversals=\'0\'>\n                    <alias target=\'/echo/*\'/>\n                    <action callback=\'echo\'/>\n                </variable>\n            </node>\n        </grammar>\n        '
        grammar = Grammar.from_xml(xml, echo=self._echo)
        parser = Parser(grammar)
        parser.execute('echo magic monkey')
        self.assertEqual(self._output, {'text': ['magic', 'monkey']})

    def test_group(self):
        xml = '<?xml version="1.0"?>\n        <grammar>\n            <node name=\'echo\'>\n                <group traversals=\'0\'>\n                    <variable name=\'text\'>\n                        <alias target=\'../../*\'/>\n                        <action callback=\'echo\'/>\n                    </variable>\n                </group>\n            </node>\n        </grammar>\n        '
        grammar = Grammar.from_xml(xml, echo=self._echo)
        parser = Parser(grammar)
        parser.execute('echo magic monkey')
        self.assertEqual(self._output, {'text': ['magic', 'monkey']})

    def test_completion(self):
        xml = '<?xml version="1.0"?>\n        <grammar>\n            <node name=\'echo\'>\n                <variable name=\'text\' candidates=\'candidates\'>\n                    <action callback=\'echo\'/>\n                </variable>\n            </node>\n        </grammar>\n        '

        def candidates(context, text):
            return [
             'monkey', 'muppet']

        grammar = Grammar.from_xml(xml, echo=self._echo, candidates=candidates)
        parser = Parser(grammar)
        context = parser.parse('echo ')
        self.assertEqual(list(context.candidates()), ['monkey', 'muppet'])

    def test_node_extension(self):
        from cly.builder import Variable

        class ABC(Variable):
            pattern = '(?i)[abc]+'

        xml = '<?xml version="1.0"?>\n        <grammar>\n            <node name=\'echo\'>\n                <abc name=\'text\'>\n                    <action callback=\'echo\'/>\n                </abc>\n            </node>\n        </grammar>\n        '
        grammar = Grammar.from_xml(xml, extra_nodes=[ABC], echo=self._echo)
        parser = Parser(grammar)
        parser.execute('echo abaabbccc')
        self.assertEqual(self._output, {'text': 'abaabbccc'})


def suite():
    import cly, cly.interactive, cly.console, cly.extra, cly.parser, cly.builder, cly.exceptions
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestXMLGrammar, 'test'))
    suite.addTest(doctest.DocTestSuite(cly))
    suite.addTest(doctest.DocTestSuite(cly.interactive))
    suite.addTest(doctest.DocTestSuite(cly.console))
    suite.addTest(doctest.DocTestSuite(cly.extra))
    suite.addTest(doctest.DocTestSuite(cly.parser))
    suite.addTest(doctest.DocTestSuite(cly.builder))
    suite.addTest(doctest.DocTestSuite(cly.exceptions))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')