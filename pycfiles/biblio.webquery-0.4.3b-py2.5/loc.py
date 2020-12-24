# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/biblio/webquery/loc.py
# Compiled at: 2009-04-28 15:06:08
"""
Querying the Library of Congress for bibliographic information.
"""
__docformat__ = 'restructuredtext en'
from basewebquery import BaseWebquery
import querythrottle
LOC_ROOTURL = 'http://z3950.loc.gov:7090/voyager?operation=searchRetrieve&version=1.1'

class LocQuery(BaseWebquery):

    def __init__(self, timeout=5.0, limits=None):
        """
                C'tor.
                """
        root_url = LOC_ROOTURL % {'key': key}
        BaseWebquery.__init__(self, root_url=root_url, timeout=timeout, limits=limits)

    def query_bibdata_by_isbn(self, isbn, format='MODS'):
        """
                Return the metadata for a publication specified by ISBN.
                """
        format = lower(format)
        assert format in ('mods', 'opacxml', 'dc', 'marcxml')
        sub_url = '&recordSchema=%(format)s&startRecord=1&maximumRecords=5&query=bath.standardIdentifier=%(isbn)s' % {'isbn': isbn, 
           'format': format}
        return self.query(sub_url)


def _doctest():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _doctest()