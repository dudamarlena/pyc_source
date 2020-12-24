# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/break_html_page.py
# Compiled at: 2010-10-16 07:02:00
"""
The module defines BreakHtmlPage class that works with the DOM model.

It is almost twice as slow than break_html_page2 !!! But it uses DOM.

This module uses html5lib to parse the HTML page
http://code.google.com/p/html5lib/

There is an option to use this class without working with html5lib (and then it
doesn't have to be present). Using the "set_dom" method to set an external DOM
object, and not using the "feed" and "close" methods.

I added the hash code of the parent Tag in the HTML tree to the identity of each
Tag object. That makes two tags equal only if they under the exact same path in
the HTML tree.
"""
from xml.dom import Node
from StringIO import StringIO
from break_page_seq import BreakPageSeq
from utills import quote_html
ENCODING = 'utf-8'
NOT_SELF_CLOSE = ('div', 'button')

def _write_elm(buff):
    """ Return a function (closure) that renders element into buff """

    def __write_elm(elm):
        """ Render an HTML element """
        if elm.nodeType == Node.ELEMENT_NODE:
            buff.write('<' + elm.nodeName.encode(ENCODING))
            if elm.attributes:
                for (name, value) in elm.attributes.items():
                    value = quote_html(value)
                    buff.write(' %s="%s"' % (
                     name.encode(ENCODING), value.encode(ENCODING)))

            if elm.hasChildNodes() or elm.nodeName in NOT_SELF_CLOSE:
                buff.write('>')
            else:
                buff.write(' />')
        elif elm.nodeType == Node.COMMENT_NODE:
            buff.write('<!-- %s -->' % elm.nodeValue.encode(ENCODING))
        else:
            buff.write(elm.nodeValue.encode(ENCODING))

    return __write_elm


def _write_close_elm(buff):
    """ Same for close element (tag) """

    def __write_close_elm(elm):
        if elm.nodeType == Node.ELEMENT_NODE and (elm.hasChildNodes() or elm.nodeName in NOT_SELF_CLOSE):
            buff.write('</%s>' % elm.nodeName.encode(ENCODING))

    return __write_close_elm


def traverse_tree(root, stop_elm=None):
    """ Experimental function, I don't use it as it is way too slow """
    _stop = False

    def _traverse_tree(root, stop_elm):
        if not root or root is stop_elm:
            traverse_tree._stop = True
            return
        yield root
        if not _stop and root.firstChild:
            for itm in _traverse_tree(root.firstChild, stop_elm):
                yield itm

        if not _stop and root.nextSibling:
            for itm in _traverse_tree(root.nextSibling, stop_elm):
                yield itm

    return _traverse_tree(root, stop_elm)


class StopTraversing(object):
    pass


class BreakHtmlPage(BreakPageSeq):
    """ Implements the BreakHtmlPage class using DOM and html5lib.
        This class will not return an overlapping HTML sections.
        """

    def close(self):
        """ Parse the HTML buffer """
        from html5lib import HTMLParser
        from html5lib import treebuilders
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('dom'))
        doc = parser.parse(self._html)
        self._html.close()
        self.set_dom(doc)

    def set_dom(self, dom):
        """ This public method is unique for this implementation of
                BreakHtmlPage. It lets the system to set an already prepared DOM object,
                so we don't need to parse the document again.
                """
        dom.normalize()
        self._orig_lst = tuple(self._traverse_tree(dom.documentElement))

    @classmethod
    def _traverse_tree(cls, root_elm, stop_elm=None, stop_at_root=True):
        """ An help method that creates an iterator that traverses a DOM tree.
                It stops in the end of the tree or when elm equal to stop_elm.
                If stop_at_root is False it will continue to the sibling of the given
                root, if exists.
                """
        elm = root_elm
        back_up = False
        while elm is not None and elm is not stop_elm:
            if not back_up:
                yield elm
            if not back_up and elm.hasChildNodes():
                back_up = False
                elm = elm.firstChild
            elif elm.nextSibling:
                back_up = False
                elm = elm.nextSibling
            else:
                back_up = True
                elm = elm.parentNode
            if stop_at_root and elm is root_elm:
                break

        return

    @classmethod
    def traverse_list(cls, elm_lst, elm_func, elm_close_func=None, stop_elm=None, parents=None):
        """ See base class documentation
                parents is for internal use only
                """
        if not elm_lst:
            return
        else:
            if parents is None:
                parents = set()
            for elm in elm_lst:
                if elm is stop_elm:
                    return StopTraversing
                if elm.parentNode in parents:
                    continue
                res = elm_func(elm)
                if res is not None:
                    return res
                res = cls.traverse_list(elm.childNodes, elm_func, elm_close_func, stop_elm, parents)
                if res is not None:
                    return res
                if elm_close_func:
                    res = elm_close_func(elm)
                    if res is not None:
                        return res
                parents.add(elm)

            return

    @classmethod
    def list2text(cls, lst, stop_elm=None):
        """ See base class documentation """
        buff = StringIO()
        cls.traverse_list(lst, _write_elm(buff), _write_close_elm(buff), stop_elm)
        return buff.getvalue()

    @classmethod
    def words_between_elements(cls, start, end):
        """ See base class documentation """
        lst = [ len(elm.nodeValue.split()) for elm in cls._traverse_tree(start, end, stop_at_root=False) if elm.nodeType == Node.TEXT_NODE if elm.nodeValue.strip()
              ]
        return sum(lst)

    @classmethod
    def get_element_name(cls, elm):
        """ Return the element (tag) name """
        return elm.nodeName

    @classmethod
    def get_element_attrs(cls, elm):
        """ Return the element (tag) attributes dictionary or None """
        if not elm.attributes:
            return None
        else:
            return elm.attributes

    def get_all_element_data(cls, elm):
        """ Return a tuple of the element name, attributes and the hash value
                of the Tag of the parent element. This will make two tags to be equal
                only if they have the same name and format attributes AND have the exact
                same path from the document root.
                """
        return (
         cls.get_element_name(elm), cls.get_element_attrs(elm),
         elm.parentNode._tag._hash if cls.is_tag_element(elm.parentNode) else None)

    @classmethod
    def is_tag_element(cls, elm):
        """ See base class documentation """
        return elm and elm.nodeType == Node.ELEMENT_NODE

    @classmethod
    def is_text_elm(cls, elm):
        """ See base class documentation """
        if elm.nodeType == Node.TEXT_NODE and elm.data.strip():
            return True
        else:
            return

    @classmethod
    def test2(cls, verbose):
        """ Add a test for the tree like functionality to the standard tests
                I make it happen mainly in the get_all_element_data method
                """
        cls.test(verbose)
        from repeat_pattern import RepeatPattern
        if verbose:
            print 'Testing tree attributes...'
        html = '<body>\n\t\t<div>\n\t\t\t<span><a>AAA</a></span>\n\t\t\t<span><a>BBB</a></span>\n\t\t</div>\n\t\t<span><a>CCC</a></span>  <!-- Should not take this occurrence -->\n\t\t</body>'
        bhp = cls()
        bhp.feed(html)
        bhp.close()
        rp = RepeatPattern()
        rp.process(tuple(bhp.get_tag_list()))
        assert rp.repeats == 2, 'Found %s occurrences' % rp.repeats


if __name__ == '__main__':
    BreakHtmlPage.test2(verbose=True)
    print 'Test Passed'