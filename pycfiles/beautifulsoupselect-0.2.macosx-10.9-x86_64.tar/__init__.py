# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomlee/.virtualenvs/beautifulsoupselect/lib/python2.7/site-packages/beautifulsoupselect/__init__.py
# Compiled at: 2014-10-01 20:22:33
import BeautifulSoup
from soupselect import select

class BeautifulSoupSelect(object):
    """
    >>> html = '<html><body><div id="foo">bar</div></body></html>'
    >>> bss = BeautifulSoupSelect(html)
    >>> bss('#foo')[0].text
    u'bar'
    """

    def __init__(self, html):
        super(BeautifulSoupSelect, self).__init__()
        self.bs = BeautifulSoup.BeautifulSoup(html)

    def __call__(self, selector):
        return select(self.bs, selector)


if __name__ == '__main__':
    import doctest
    doctest.testmod()