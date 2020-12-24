# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/lists.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: lists

TODO
    
"""
from parser import ParagraphToken, XMLElement, PrefixToken
LIST_TAGS = {'*': ('ul', 'bullet'), '-': ('ul', 'dash'), '#': ('ol', 'ordered')}
LISTS = 'lists'
LIST_RESULT = 'list result'

def _list_to_xhtml(list, is_sublist=False):
    xhtml = XMLElement('div')
    if is_sublist:
        container = None
    else:
        container = xhtml
    for (type, value) in list:
        if type == '':
            value.xhtml.tag = 'li'
            container = value.xhtml
            xhtml.append(value.xhtml)
        else:
            sublist = _list_to_xhtml(value, True)
            sublist.tag = LIST_TAGS[type][0]
            sublist.attributes['class'] = LIST_TAGS[type][1]
            if container is None:
                container = XMLElement('li')
                xhtml.append(container)
            container.append(sublist)

    return xhtml


class ListResultToken(ParagraphToken):
    __module__ = __name__

    def __init__(self, lists, token):
        ParagraphToken.__init__(self, token)
        self._list = XMLElement()
        self.xhtml.append(self._list)
        self.lists = lists

    def do_extended_close(self, inserted_token):
        self._list.content = _list_to_xhtml(self.lists).content
        inserted_token.xhtml.append(*self.xhtml.content)

    def is_a(self, *capabilities):
        return LIST_RESULT in capabilities or ParagraphToken.is_a(self, *capabilities)


class ListToken(PrefixToken):
    __module__ = __name__

    def __init__(self, token, *args, **kwargs):
        PrefixToken.__init__(self, token, *args, **kwargs)
        self.lists = []

    def do_prefix(self, new_token):
        assert len(self.lists) == 0
        if len(self.result) > 0 and self.result[(-1)].is_a(LIST_RESULT):
            self.lists = self.result.pop().lists
        current_list = self.lists
        for list_type in self.token[:-1]:
            if len(current_list) == 0 or current_list[(-1)][0] != list_type:
                new_list = []
                current_list.append((list_type, new_list))
                current_list = new_list
            else:
                current_list = current_list[(-1)][1]

        current_list.append(('', new_token))
        self.result.append(ListResultToken(self.lists, self.token))

    def render(self, new_token):
        PrefixToken.render(self, new_token)


def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[LISTS] = (
     10, '^[#*-]+[ \\t]', ListToken, dict(preference=30))