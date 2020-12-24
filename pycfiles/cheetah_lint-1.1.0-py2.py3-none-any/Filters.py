# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/Filters.py
# Compiled at: 2019-09-22 10:12:27
import unittest, Cheetah.Template, Cheetah.Filters

class BasicMarkdownFilterTest(unittest.TestCase):
    """
        Test that our markdown filter works
    """

    def test_BasicHeader(self):
        template = '\n#from Cheetah.Filters import Markdown\n#transform Markdown\n$foo\n\nHeader\n======\n        '
        expected = '<p>bar</p>\n<h1>Header</h1>'
        try:
            template = Cheetah.Template.Template(template, searchList=[{'foo': 'bar'}])
            template = str(template)
            assert template == expected
        except ImportError as ex:
            print '>>> We probably failed to import markdown, bummer %s' % ex
            return
        except Exception:
            raise


class BasicCodeHighlighterFilterTest(unittest.TestCase):
    """
        Test that our code highlighter filter works
    """

    def test_Python(self):
        template = "\n#from Cheetah.Filters import CodeHighlighter\n#transform CodeHighlighter\n\ndef foo(self):\n    return '$foo'\n        "
        template = Cheetah.Template.Template(template, searchList=[{'foo': 'bar'}])
        template = str(template)
        assert template, (template, 'We should have some content here...')

    def test_Html(self):
        template = '\n#from Cheetah.Filters import CodeHighlighter\n#transform CodeHighlighter\n\n<html><head></head><body>$foo</body></html>\n        '
        template = Cheetah.Template.Template(template, searchList=[{'foo': 'bar'}])
        template = str(template)
        assert template, (template, 'We should have some content here...')