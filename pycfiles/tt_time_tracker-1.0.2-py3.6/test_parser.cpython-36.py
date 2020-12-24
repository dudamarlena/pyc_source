# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/timeline/test_parser.py
# Compiled at: 2020-03-10 16:51:28
# Size of source mod 2**32: 1626 bytes
from unittest import TestCase
from lark import Lark

class TestLarkParser(TestCase):

    def test_parse_tree_creation(self):
        timeline_grammar = '\n            start: instruction+\n            instruction: timeentry NEWLINE billingstatus\n            \n            timeentry: "- " time\n            billingstatus: billing\n                        \n            billing: ( DONOTBILL | BILL )\n            time: DIGIT ~ 2 ":" DIGIT ~ 2\n            \n            DONOTBILL: "do"\n            BILL: "bill"\n            DIGIT: "0".."9" \n            %import common.NEWLINE\n            %import common.WS\n            %import common.WS_INLINE\n            %ignore WS\n        '
        timeline_example = '\n            -  16:00\n                        bill\n            -  18:00\n                   do\n        '
        parser = Lark(timeline_grammar)
        lark_parse_tree = parser.parse(timeline_example)
        for entry in lark_parse_tree.children:
            print(entry)

        self.assertTrue(len(lark_parse_tree.children) == 2)
        sample_grammar = '\n                start: instruction+\n                instruction: MOVEMENT NUMBER            -> movement\n                           | "c" COLOR [COLOR]          -> change_color\n                           | "fill" code_block          -> fill\n                           | "repeat" NUMBER code_block -> repeat\n                code_block: "{" instruction+ "}"\n                MOVEMENT: "f"|"b"|"l"|"r"\n                COLOR: LETTER+\n                %import common.LETTER\n                %import common.INT -> NUMBER\n                %import common.WS\n            '