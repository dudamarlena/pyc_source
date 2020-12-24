# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/break_page_seq.py
# Compiled at: 2010-10-16 07:02:00
"""
This abstract base class adds to BreakPageBase the methods that will be common
to all the implementations that work by breaking the HTML page to a list of
elements. The two implementations I have now work this way.
"""
from StringIO import StringIO
from break_page_base import BreakPageBase
from tag_tools import Tag

class BreakPageSeq(BreakPageBase):
    """ Abstract base class for the BreakXXX classes that works with an element
        list.
        """

    def __init__(self):
        BreakPageBase.__init__(self)
        self._html = None
        self._orig_lst = None
        self._index_lst = None
        return

    def element_by_tag_index(self, index):
        """ See base class documentation """
        return self._orig_lst[self._index_lst[index]]

    def feed(self, data):
        """ See base class documentation """
        if not self._html:
            self._html = StringIO()
        self._html.write(data)

    def clear(self):
        """ See base class documentation """
        if self._html:
            self._html.close()
        self._html = None
        self._orig_lst = None
        self._index_lst = None
        return

    def get_tag_list(self):
        """ See base class documentation
                The method adds each Tag object to the element that creates it under
                the _tag attribute.
                """
        if not self._orig_lst:
            return
        self._index_lst = []
        for (index, elm) in enumerate(self._orig_lst):
            if self.is_tag_element(elm):
                tag = Tag(*self.get_all_element_data(elm))
                elm._tag = tag
                if (not self.include_tags or tag in self.include_tags) and (not self.exclude_tags or tag not in self.exclude_tags):
                    self._index_lst.append(index)
                    yield tag

    def get_text_list(self, lst):
        """ See base class documentation """
        if not self._orig_lst or not self._index_lst or not lst:
            return
        else:
            for (index, entry) in enumerate(lst):
                start = self._index_lst[entry[0]]
                end = self._index_lst[entry[1]] + 1
                if index < len(lst) - 1:
                    next = self._orig_lst[self._index_lst[lst[(index + 1)][0]]]
                else:
                    next = None
                yield (
                 self._orig_lst[start:end], next)

            return

    @classmethod
    def test(cls, verbose=False):
        """ Testing this class - This is a very limited test!

                I'm not testing the HTML overlap prevention (yet).
                An example of it working is if processing the page:
                http://docs.python.org/dev/whatsnew/2.6.html
                """
        bhp = cls()
        f = open('test/google.html')
        for line in f.readlines():
            bhp.feed(line)

        bhp.close()
        if verbose:
            print 'Test the exclusion feature, the inclusion hopefully works the same'
        bhp.exclude_tags += (Tag('em'), Tag('a', {'class': 'gb2'}))
        tag_lst = bhp.get_tag_list()
        assert Tag('html', {'class': 'bar'}) not in tag_lst
        assert Tag('a', {'class': 'gb2'}) not in tag_lst
        if verbose:
            print "Manually find the 'known pattern' indices"
        start_lst = []
        end_lst = []
        start_tag = Tag('li', {'class': 'g'})
        end_tag = Tag('span', {'class': 'gl'})
        start_lst = [ index for (index, tag) in enumerate(tag_lst) if tag == start_tag ]
        end_lst = [ index for (index, tag) in enumerate(tag_lst) if tag == end_tag ]
        assert len(start_lst) == len(end_lst)
        lst = zip(start_lst, end_lst)
        if verbose:
            print 'Make sure we are getting the appropriate HTML sections'
        for (sub_lst, next) in bhp.get_text_list(lst):
            html = list2text(sub_lst, next)
            assert html.startswith('<li class=g>')
            assert html.endswith('</div>')
            assert html[14:].find('<li class=g>') == -1