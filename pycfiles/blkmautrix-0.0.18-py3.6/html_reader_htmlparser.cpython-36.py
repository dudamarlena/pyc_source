# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/formatter/html_reader_htmlparser.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1993 bytes
from typing import Dict, List, Tuple
from html.parser import HTMLParser

class HTMLNode(list):
    tag: str
    text: str
    tail: str
    attrib: Dict[(str, str)]

    def __repr__(self) -> str:
        return f"HTMLNode(tag='{self.tag}', attrs={self.attrib}, text='{self.text}', tail='{self.tail}', children={list(self)})"

    def __init__(self, tag, attrs):
        super().__init__()
        self.tag = tag
        self.text = ''
        self.tail = ''
        self.attrib = dict(attrs)


class NodeifyingParser(HTMLParser):
    void_tags = ('area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input',
                 'link', 'meta', 'param', 'source', 'track', 'wbr')
    stack: List[HTMLNode]

    def __init__(self):
        super().__init__()
        self.stack = [HTMLNode('html', [])]

    def handle_starttag(self, tag: str, attrs: List[Tuple[(str, str)]]) -> None:
        node = HTMLNode(tag, attrs)
        self.stack[(-1)].append(node)
        if tag not in self.void_tags:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[(-1)].append(HTMLNode(tag, attrs))

    def handle_endtag(self, tag: str) -> None:
        if tag == self.stack[(-1)].tag:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if len(self.stack[(-1)]) > 0:
            self.stack[(-1)][(-1)].tail += data
        else:
            self.stack[(-1)].text += data

    def error(self, message: str) -> None:
        pass


def read_html(data: str) -> HTMLNode:
    parser = NodeifyingParser()
    parser.feed(data)
    return parser.stack[0]