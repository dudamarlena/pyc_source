# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/test/test_isbndb.py
# Compiled at: 2009-05-04 18:59:08
"""
Tests for biblio.webquery.isbndb, using nose.
"""
from biblio.webquery import isbndb
BAD_STATUS_XML = '<?xml version="1.0" encoding="UTF-8" ?>\n\t<rsp xmlns="http://worldcat.org/xid/isbn/" stat="invalidId"/>'
SIMPLE_ONE_XML = '<?xml version="1.0" encoding="UTF-8"?>\n\t<ISBNdb server_time="2005-07-29T02:41:22">\n\t <BookList total_results="1" page_size="10" page_number="1" shown_results="1">\n\t  <BookData book_id="law_and_disorder" isbn="0210406240">\n\t   <Title>Law and disorder</Title>\n\t   <TitleLong>\n\t    Law and disorder: law enforcement in television network news\n\t   </TitleLong>\n\t   <AuthorsText>V. M. Mishra</AuthorsText>\n\t   <PublisherText publisher_id="asia_pub_house">\n\t    New York: Asia Pub. House, c1979.\n\t   </PublisherText>\n\t   <Details dewey_decimal="302.2/3"\n\t            dewey_decimal_normalized="302.23"\n\t            lcc_number="PN4888"\n\t            language="eng"\n\t            physical_description_text="x, 127 p. ; 22 cm."\n\t            edition_info=""\n\t            change_time="2004-10-19T23:52:56"\n\t            price_time="2005-07-29T02:06:41" />\n\t  </BookData>\n\t </BookList>\n\t</ISBNdb>'

class test_isbndb_xml_to_bibrecords(object):

    def test_simple_one(self):
        recs = isbndb.isbndb_xml_to_bibrecords(SIMPLE_ONE_XML)
        assert len(recs) == 1