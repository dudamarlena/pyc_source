# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/break_html_page2.py
# Compiled at: 2010-10-16 07:02:00
"""
A way to break an HTML list without using external library.
I am using regular expressions, it is working significantly faster than with
html5lib.

I don't really need to "parse" the page, only to find all the tags.

The regular expression is based on
http://kevin.deldycke.com/2008/07/python-ultimate-regular-expression-to-catch-html-tags/
"""
import re
from collections import deque
from break_page_seq import BreakPageSeq
from utills import iter2tuple

class ElmStruct(object):

    def __repr__(self):
        """ For debugging """
        if self.attrs_dict:
            attrs = ' ' + (',').join('%s="%s"' % (name, val) for (name, val) in self.attrs_dict.items())
        else:
            attrs = ''
        return '<%s%s>' % (self.name, attrs)


class BreakHtmlPage(BreakPageSeq):
    """ Implements the BreakPage class using regular expressions.
        This class should be used with RepeatPattern in order to get a repetitive
        pattern in an HTML text.
        This class will not return an overlapping HTML sections.
        """
    TAGS_RE = '\n\t<\n\t(?P<closing>\\/)?\n\t(?P<name>\\w+)\n\t(?P<attrs>(?:\\s+\\w+(?:\\s*=\\s*(?:".*?"|\'.*?\'|[^\'">\\s]+))?)+\\s*|\\s*)\n\t(?P<self_closing>\\/)?\n\t>\n\t'
    ATTRS_RE = '\n\t\\s+\n\t(?P<name>\\w+)\n\t(?:\\s*=\\s*\n\t(?:\n\t"(?P<val1>.*?)"\n\t|\n\t\'(?P<val2>.*?)\'\n\t|\n\t(?P<val3>[^\'">\\s]+\n\t)))?\n\t'
    g_html = None

    def __init__(self):
        BreakPageSeq.__init__(self)
        self._tags_re = re.compile(self.TAGS_RE, re.I | re.X)
        self._attrs_re = re.compile(self.ATTRS_RE, re.I | re.X)

    @iter2tuple
    def _parse(self, text):
        """ Create the list of tags from the text. """
        last_tag = None
        for tag in self._tags_re.finditer(text):
            elm_struct = ElmStruct()
            elm_struct.name = tag.group('name')
            elm_struct.closing = bool(tag.group('closing'))
            elm_struct.self_closing = bool(tag.group('self_closing'))
            elm_struct.start = tag.start()
            elm_struct.end = tag.end()
            elm_struct.close_tag = elm_struct
            if last_tag:
                last_tag.next = elm_struct
            last_tag = elm_struct
            if tag.group('attrs'):
                elm_struct.attrs_dict = dict((attr.group('name'), attr.group('val1') or attr.group('val2') or attr.group('val3')) for attr in self._attrs_re.finditer(tag.group('attrs')))
            else:
                elm_struct.attrs_dict = None
            yield elm_struct

        return

    def _insert_close_tags(self, lst):
        """ close_tag of a TagSturct will be the closing tag if any.
                """
        balance = deque()
        for tag in lst:
            if not tag.closing and not tag.self_closing:
                balance.appendleft(tag)
            elif tag.closing:
                index = 0
                while index < len(balance) and balance[index].name != tag.name:
                    index += 1

                if index < len(balance):
                    balance[index].close_tag = tag
                    for i in range(index + 1):
                        balance.popleft()

    def close(self):
        """ Parse the HTML buffer """
        self.__class__.g_html = self._html.getvalue()
        self._html.close()
        self._orig_lst = self._parse(self.g_html)
        self._insert_close_tags(self._orig_lst)

    @classmethod
    def traverse_list(cls, elm_lst, elm_func, elm_close_func=None, stop_elm=None):
        """ See base class documentation """
        if not elm_lst:
            return
        else:
            end = max(elm.close_tag.end for elm in elm_lst)
            elm = elm_lst[0]
            while elm and elm.start < end:
                if stop_elm and elm.end > stop_elm.start:
                    break
                res = elm.closing or elm_func(elm)
                if res is not None:
                    return res
                elif elm_close_func:
                    res = elm_close_func(elm)
                    if res is not None:
                        return res
                elm = elm.next

            return

    @classmethod
    def list2text(cls, lst, stop_elm=None):
        """ See base class documentation """
        if not lst:
            return ''
        start = lst[0].start
        end = max(itm.close_tag.end for itm in lst)
        if stop_elm:
            end = min(end, stop_elm.start)
        return cls.g_html[start:end]

    @classmethod
    def words_between_elements(cls, start, end):
        """ See base class documentation """
        counter = 0
        elm = start
        while elm != end:
            if elm.next:
                counter += len(cls.g_html[elm.end:elm.next.start].split())
            elm = elm.next

        return counter

    @classmethod
    def get_element_name(cls, elm):
        """ See base class documentation """
        return elm.name

    @classmethod
    def get_element_attrs(cls, elm):
        """ See base class documentation """
        return elm.attrs_dict

    def get_all_element_data(cls, elm):
        """ Return a tuple of the element name and attributes """
        return (
         cls.get_element_name(elm), cls.get_element_attrs(elm))

    @classmethod
    def is_tag_element(cls, elm):
        """ See base class documentation """
        return not elm.closing

    @classmethod
    def is_text_elm(cls, elm):
        """ See base class documentation """
        if not elm.closing and not elm.self_closing and elm.end < elm.close_tag.end:
            if cls.g_html[elm.end:elm.next.start].strip():
                return True
        return


if __name__ == '__main__':
    BreakHtmlPage.test(verbose=True)
    print 'Test Passed'