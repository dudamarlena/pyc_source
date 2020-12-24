# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ledsign/am03127/parsers.py
# Compiled at: 2014-04-16 03:40:04
"""
Message parsers for easier human interfacing
"""
from .messages import *
import bbcode

class BaseParser(object):
    """
        A general parser that renders a given class
        """
    TARGET = object

    def __init__(self):
        pass

    def parse(self, data):
        """
                The actual parsing takes place here, this must be subclassed and the kwargs returned
                """
        return {}

    def render(self, data):
        target_kwargs = self.parse(data)
        instance = self.TARGET(**target_kwargs)
        return instance


class PageContentBBCodeParser(BaseParser):
    """
        Parse page content from BBCode
        """
    TARGET = PageContent

    def __init__(self):

        def _bb_dummy(tagname, value, options, parent, context):
            pass

        self.bbcode_parser = bbcode.Parser()
        self.bbcode_parser.add_formatter('font', _bb_dummy, standalone=True)
        self.bbcode_parser.add_formatter('bell', _bb_dummy, standalone=True)
        self.bbcode_parser.add_formatter('color', _bb_dummy, standalone=True)
        self.bbcode_parser.add_formatter('graphic', _bb_dummy, standalone=True)
        self.bbcode_parser.add_formatter('char', _bb_dummy, standalone=True)
        self.bbcode_parser.add_formatter('column', _bb_dummy, standalone=True)
        self.bbcode_parser.add_formatter('date', _bb_dummy, standalone=True)
        self.bbcode_parser.add_formatter('time', _bb_dummy, standalone=True)

    def parse(self, data):
        target_data = []
        tokens = self.bbcode_parser.tokenize(data)
        for token_type, tag_name, tag_options, token_text in tokens:
            if token_type == self.bbcode_parser.TOKEN_TAG_START:
                if tag_name in ('date', 'time'):
                    key = 'datetime'
                    value = tag_name
                else:
                    key = tag_name
                    value = tag_options.get(tag_name)
                target_data.append({key: value})
            elif token_type == self.bbcode_parser.TOKEN_DATA:
                target_data.append(token_text)

        target_kwargs = {'data': target_data}
        return target_kwargs