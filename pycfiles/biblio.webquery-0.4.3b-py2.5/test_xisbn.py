# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/test/test_xisbn.py
# Compiled at: 2009-05-04 06:00:11
"""
Tests for biblio.webquery.xisbn, using nose.
"""
from biblio.webquery import xisbn
BAD_STATUS_XML = '<?xml version="1.0" encoding="UTF-8" ?>\n\t<rsp xmlns="http://worldcat.org/xid/isbn/" stat="invalidId"/>'
SIMPLE_ONE_XML = '<?xml version="1.0" encoding="UTF-8"?>\n<rsp xmlns="http://worldcat.org/xid/isbn/" stat="ok">\n\t<isbn title="Learning Python" form="BA" year="2004" lang="eng" ed="2nd ed." author="Lutz, Mark." publisher="O\'Reilly">0596002815</isbn>\n</rsp>'

class xtest_xisbn_xml_to_dicts(object):

    def test_bad_status(self):
        try:
            recs = xisbn.xisbn_xml_to_dicts(BAD_STATUS_XML)
            assert False, 'should fail if reading document with bad status'
        except:
            pass

    def test_simple_one(self):
        recs = xisbn.xisbn_xml_to_dicts(SIMPLE_ONE_XML)