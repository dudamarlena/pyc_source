# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/griflet/venv/lib/python3.4/site-packages/test/parsertest.py
# Compiled at: 2017-02-20 22:22:31
# Size of source mod 2**32: 3068 bytes
from pyrev.parser import Parser
import unittest
from logging import getLogger, DEBUG
local_logger = getLogger(__name__)

def _enable_local_logger():
    from logging import StreamHandler
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    local_logger.setLevel(DEBUG)
    local_logger.addHandler(handler)


def _disable_local_logger():
    from logging import NullHandler
    local_logger.addHandler(NullHandler())


def _msg(problems):
    if len(problems) > 1:
        return 'Multiple problems happned.\n' + '\n'.join(map(lambda problem: str(problem), problems))
    else:
        if len(problems) == 1:
            return str(problems[0])
        return ''


class ParserTest(unittest.TestCase):

    def test_parser_basic(self):
        parser = Parser(project=None, logger=local_logger)
        parser._parse_file_inter(['= title', 'world'], 0, 'fake.re')
        self.assertEqual(0, len(parser.reporter.problems), msg=_msg(parser.reporter.problems))

    def test_block_param_bs1(self):
        content = '//footnote[fn][C-\\]]'
        parser = Parser(project=None, logger=local_logger)
        parser._parse_file_inter(['= title', content], 0, 'fake.re')
        self.assertEqual(0, len(parser.reporter.problems), msg=_msg(parser.reporter.problems))

    def test_block_param_bs2(self):
        content = '//footnote[fn][@<b>{C-\\]}]'
        parser = Parser(project=None, logger=local_logger)
        parser._parse_file_inter(['= title', content], 0, 'fake.re')
        self.assertEqual(0, len(parser.reporter.problems), msg=_msg(parser.reporter.problems))
        self.assertEqual(1, len(parser.all_blocks))
        block = parser.all_blocks[0]
        self.assertEqual(2, len(block.params))
        self.assertEqual(('footnote', 'fn', 2), (
         block.name, block.params[0], block.line_num))
        self.assertEqual(1, len(parser.all_inlines))
        inline = parser.all_inlines[0]
        self.assertEqual(('b', 'C-]', 2, 24), (
         inline.name, inline.raw_content, inline.line_num,
         inline.position))

    def test_block_param_bs3(self):
        content = '//footnote[fn][@<b>{C-]}]'
        parser = Parser(project=None, logger=local_logger)
        parser._parse_file_inter(['= title', content], 0, 'fake.re')
        self.assertEqual(1, len(parser.reporter.problems))
        self.assertEqual(1, len(parser.all_blocks))
        block = parser.all_blocks[0]
        self.assertEqual(2, len(block.params))
        self.assertEqual(('footnote', 'fn', 2), (
         block.name, block.params[0], block.line_num))
        inline = parser.all_inlines[0]
        self.assertEqual(('b', 'C-]', 2), (
         inline.name, inline.raw_content, inline.line_num))


if __name__ == '__main__':
    _disable_local_logger()
    unittest.main()