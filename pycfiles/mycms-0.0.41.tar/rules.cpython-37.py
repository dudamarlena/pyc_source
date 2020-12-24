# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/creole/creole2html/rules.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 7313 bytes
"""
    Creole Rules for parser
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2008-2013 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
from __future__ import division, absolute_import, print_function, unicode_literals
import re

class InlineRules(object):
    __doc__ = '\n    All inline rules\n    '
    proto = 'http|https|ftp|nntp|news|mailto|telnet|file|irc'
    url = '(?P<url>\n            (^ | (?<=\\s))\n            (?P<escaped_url>~)?\n            (?P<url_target> (?P<url_proto> %s )://[^$\\s]+ )\n        )' % proto
    link = '(?P<link>\n            \\[\\[\n            (?P<link_target>.+?) \\s*\n            ([|] \\s* (?P<link_text>.+?) \\s*)?\n            ]]\n        )'
    image = '(?P<image>\n            {{\n            (?P<image_target>.+?) \\s*\n            (\\| \\s* (?P<image_text>.+?) \\s*)?\n            }}\n        )(?i)'
    macro_inline = '\n        (?P<macro_inline>\n        << \\s* (?P<macro_inline_start>\\w+) \\s* (?P<macro_inline_args>.*?) \\s* >>\n        (?P<macro_inline_text>(.|\\n)*?)\n        <</ \\s* (?P=macro_inline_start) \\s* >>\n        )\n    '
    macro_tag = '(?P<macro_tag>\n            <<(?P<macro_tag_name> \\w+) (?P<macro_tag_args>.*?) \\s* /*>>\n        )'
    pre_inline = '(?P<pre_inline> {{{ (?P<pre_inline_text>.*?) }}} )'
    emphasis = '(?P<emphasis>(?<!:)// (?P<emphasis_text>.+?) (?<!:)// )'
    strong = '(?P<strong>\\*\\* (?P<strong_text>.+?) \\*\\* )'
    monospace = '(?P<monospace> \\#\\# (?P<monospace_text>.+?) \\#\\# )'
    superscript = '(?P<superscript> \\^\\^ (?P<superscript_text>.+?) \\^\\^ )'
    subscript = '(?P<subscript> ,, (?P<subscript_text>.+?) ,, )'
    underline = '(?P<underline> __ (?P<underline_text>.+?) __ )'
    delete = '(?P<delete> ~~ (?P<delete_text>.+?) ~~ )'
    small = '(?P<small>-- (?P<small_text>.+?) -- )'
    linebreak = '(?P<linebreak> \\\\\\\\ )'
    escape = '(?P<escape> ~ (?P<escaped_char>\\S) )'
    char = '(?P<char> . )'


class BlockRules(object):
    __doc__ = '\n    All used block rules.\n    '
    macro_block = '\n        (?P<macro_block>\n        << \\s* (?P<macro_block_start>\\w+) \\s* (?P<macro_block_args>.*?) \\s* >>\n        (?P<macro_block_text>(.|\\n)*?)\n        <</ \\s* (?P=macro_block_start) \\s* >>\n        )\n    '
    line = '(?P<line> ^\\s*$ )'
    head = '(?P<head>\n        ^\n        (?P<head_head>=+) \\s*\n        (?P<head_text> .*? )\n        (=|\\s)*?$\n    )'
    separator = '(?P<separator> ^ \\s* ---- \\s* $ )'
    pre_block = '(?P<pre_block>\n            ^{{{ \\s* $\n            (?P<pre_block_text>\n                ([\\#]!(?P<pre_block_kind>\\w*?)(\\s+.*)?$)?\n                (.|\\n)+?\n            )\n            ^}}})\n        '
    list = '(?P<list>\n        ^ [ \\t]* ([*][^*\\#]|[\\#][^\\#*]).* $\n        ( \\n[ \\t]* [*\\#]+.* $ )*\n    )'
    table = '^ \\s*(?P<table>\n            [|].*? \\s*\n            [|]?\n        ) \\s* $'
    re_flags = re.VERBOSE | re.UNICODE | re.MULTILINE

    def __init__(self, blog_line_breaks=True):
        if blog_line_breaks:
            self.text = '(?P<text> .+ ) (?P<break> (?<!\\\\)$\\n(?!\\s*$) )?'
        else:
            self.text = '(?P<space> (?<!\\\\)$\\n(?!\\s*$) )? (?P<text> .+ )'
        self.rules = (
         self.macro_block,
         self.line, self.head, self.separator,
         self.pre_block, self.list,
         self.table, self.text)


class SpecialRules(object):
    __doc__ = '\n    re rules witch not directly used as inline/block rules.\n    '
    item = '^ \\s* (?P<item>\n        (?P<item_head> [\\#*]+) \\s*\n        (?P<item_text> .*?)\n    ) \\s* $'
    cell = '\n            \\| \\s*\n            (\n                (?P<head> [=][^|]+ ) |\n                (?P<cell> (  %s | [^|])+ )\n            ) \\s*\n        ' % '|'.join([
     InlineRules.link,
     InlineRules.macro_inline, InlineRules.macro_tag,
     InlineRules.image,
     InlineRules.pre_inline])
    pre_escape = ' ^(?P<indent>\\s*) ~ (?P<rest> \\}\\}\\} \\s*) $'


INLINE_FLAGS = re.VERBOSE | re.UNICODE
INLINE_RULES = (
 InlineRules.link, InlineRules.url,
 InlineRules.macro_inline, InlineRules.macro_tag,
 InlineRules.pre_inline, InlineRules.image,
 InlineRules.strong, InlineRules.emphasis,
 InlineRules.monospace, InlineRules.underline,
 InlineRules.superscript, InlineRules.subscript,
 InlineRules.small, InlineRules.delete,
 InlineRules.linebreak,
 InlineRules.escape, InlineRules.char)

def _verify_rules(rules, flags):
    """
    Simple verify the rules -> try to compile it ;)
    
    >>> _verify_rules(INLINE_RULES, INLINE_FLAGS)
    Rule test ok.
    
    >>> block_rules = BlockRules()   
    >>> _verify_rules(block_rules.rules, block_rules.re_flags)
    Rule test ok.
    """
    rule_list = []
    for rule in rules:
        try:
            re.compile(rule, flags)
            rule_list.append(rule)
            re.compile('|'.join(rule_list), flags)
        except Exception as err:
            try:
                print(' *** Error with rule:')
                print(rule)
                print(' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
                raise
            finally:
                err = None
                del err

    print('Rule test ok.')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
    print('--------------------------------------------------------------------------------')