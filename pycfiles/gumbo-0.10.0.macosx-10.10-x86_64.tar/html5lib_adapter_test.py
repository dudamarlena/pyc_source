# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/gumbo/html5lib_adapter_test.py
# Compiled at: 2015-04-30 22:50:43
"""Tests for the Gumbo => Html5lib adapter."""
import codecs, collections, glob, os, re, StringIO, unittest, warnings
from html5lib import treebuilders
import html5lib_adapter
TREEBUILDER = treebuilders.getTreeBuilder('dom')
TESTDATA_BASE_PATH = os.path.join(os.path.split(__file__)[0], '..', '..')

def convertTreeDump(data):
    return ('\n').join(convertExpected(data, 3).split('\n')[1:])


def html5lib_test_files():
    return glob.glob(os.path.join(TESTDATA_BASE_PATH, 'testdata', 'tree-construction', '*.dat'))


class TestData(object):

    def __init__(self, filename):
        self.f = codecs.open(filename, encoding='utf8')

    def __iter__(self):
        data = collections.defaultdict(lambda : None)
        key = None
        for line in self.f:
            heading = self.isSectionHeading(line)
            if heading:
                if data and heading == 'data':
                    data[key] = data[key][:-1]
                    yield self.normaliseOutput(data)
                    data = collections.defaultdict(lambda : None)
                key = heading
                data[key] = ''
            elif key is not None:
                data[key] += line

        if data:
            yield self.normaliseOutput(data)
        return

    def isSectionHeading(self, line):
        """If the current heading is a test section heading return the heading,
    otherwise return False"""
        if line.startswith('#'):
            return line[1:].strip()
        else:
            return False

    def normaliseOutput(self, data):
        for key, value in data.iteritems():
            if value.endswith('\n'):
                data[key] = value[:-1]

        return data


def convertExpected(data, stripChars):
    """convert the output of str(document) to the format used in the testcases"""
    data = data.split('\n')
    rv = []
    for line in data:
        if line.startswith('|'):
            rv.append(line[stripChars:])
        else:
            rv.append(line)

    return ('\n').join(rv)


def reformatTemplateContents(expected):
    lines = expected.split('\n')
    retval = []
    template_indents = []
    for line in lines:
        line_stripped = line.strip()
        indent = len(line) - len(line_stripped)
        if line_stripped == 'content':
            template_indents.append(indent)
            continue
        while template_indents and indent <= template_indents[(-1)]:
            template_indents.pop()

        if template_indents:
            line = line[2 * len(template_indents):]
        retval.append(line)

    return ('\n').join(retval)


class Html5libAdapterTest(unittest.TestCase):
    """Adapter between Gumbo and the html5lib tests.

  This works through a bit of magic.  It's an empty class at first, but then
  buildTestCases runs through the test files in html5lib, and adds a
  method to this class for each one.  That method acts like
  test_parser.TestCase.runParserTest, running a parse, serializing the tree, and
  comparing it to the expected output.

  The vague name is so nosetests doesn't try to run it as a test.
  """

    def impl(self, inner_html, input, expected, errors):
        p = html5lib_adapter.HTMLParser(tree=TREEBUILDER(namespaceHTMLElements=True))
        if inner_html:
            document = p.parseFragment(StringIO.StringIO(input), inner_html.replace('math ', 'mathml '))
        else:
            document = p.parse(StringIO.StringIO(input))
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            output = convertTreeDump(p.tree.testSerializer(document))
        expected = re.compile('^(\\s*)<(\\S+)>', re.M).sub('\\1<html \\2>', convertExpected(expected, 2))
        expected = reformatTemplateContents(expected)
        error_msg = ('\n').join(['\n\nInput:', input, '\nExpected:', expected,
         '\nReceived:', output])
        self.assertEquals(expected, output, error_msg.encode('ascii', 'xmlcharrefreplace') + '\n')


def BuildTestCases(cls):
    for filename in html5lib_test_files():
        test_name = os.path.basename(filename).replace('.dat', '')
        for i, test in enumerate(TestData(filename)):
            if '<noscript>' in test['data']:
                continue
            if '<command>' in test['data']:
                continue

            def test_func(self, inner_html=test['document-fragment'], input=test['data'], expected=test['document'], errors=test.get('errors', '').split('\n')):
                return self.impl(inner_html, input, expected, errors)

            test_func.__name__ = 'test_%s_%d' % (test_name, i + 1)
            setattr(cls, test_func.__name__, test_func)


if __name__ == '__main__':
    BuildTestCases(Html5libAdapterTest)
    unittest.main()