# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\typepad2blogger\test\test_mt.py
# Compiled at: 2008-05-15 23:37:55
from typepad2blogger import mt
import unittest, os.path
from pkg_resources import Requirement, resource_filename
api_datafile = resource_filename(Requirement.parse('typepad2blogger'), 'typepad2blogger/test/data/api.example.data')
tp_datafile = resource_filename(Requirement.parse('typepad2blogger'), 'typepad2blogger/test/data/typepad.export.data')
api_example_data = file(api_datafile, 'rb').read()
typepad_export_data = file(tp_datafile, 'rb').read()
entry_separator = '--------'
field_separator = '-----'

class TestInitFromBasestring(unittest.TestCase):

    def setUp(self):
        self.api_data = api_example_data
        self.api_entry = api_example_data.split(entry_separator)[0]
        self.api_export = api_example_data
        fields = self.api_entry.split(field_separator)
        self.api_metadata = fields.pop(0)
        self.api_body = fields.pop(0)
        self.api_extendedbody = fields.pop(0)
        self.api_comment1 = fields.pop(0)
        self.api_comment2 = fields.pop(0)
        self.api_ping = fields.pop(0)
        self.tp_data = typepad_export_data
        self.tp_entry = typepad_export_data.split(entry_separator)[0]
        self.tp_export = typepad_export_data
        fields = self.tp_entry.split(field_separator)
        self.tp_metadata = fields.pop(0)
        self.tp_body = fields.pop(0)
        self.tp_extendedbody = fields.pop(0)
        self.tp_excerpt = fields.pop(0)
        self.tp_keywords = fields.pop(0)
        del fields

    def testMetadataFromAPI(self):
        """ Make sure we get a metadata from api data """
        m = mt.metadata(self.api_metadata)
        self.assertEqual(len(m.keys()), 5)
        self.assert_(isinstance(m, dict))
        self.assert_(isinstance(m['CATEGORY'], list))
        self.assert_(isinstance(m, mt.MoveableType))

    def testMetadataFromTP(self):
        """ Make sure we get a metadata from typepad data """
        m = mt.metadata(self.tp_metadata)
        self.assertEqual(len(m.keys()), 8)
        self.assert_(isinstance(m, dict))
        self.assert_(isinstance(m['CATEGORY'], list))
        self.assert_(isinstance(m, mt.MoveableType))

    def testBodyFromAPI(self):
        """ Make sure we get a body from api data """
        b = mt.body(self.api_body)
        self.assertEqual(unicode(b), 'This is the body.\n')
        self.assert_(isinstance(b, mt.MoveableType))

    def testBodyFromTP(self):
        """ Make sure we get a body from typepad data """
        b = mt.body(self.tp_body)
        self.assertEqual(unicode(b), "<p>So far, I see that the titling system is annoying. I guess I will have to pay more to get a custom domain.</p>\n\n<p>Just checked, and my domain name is in fact available.</p>\n\n<p>This is only the second week of grocery shopping on a budget -- $80 -- and already I have gone over. I have spent $90. But I think it's good to have some flexibility. I went over in order to take advantage of good deals with week on hams due to the Easter holiday, and I'm going to go over further when I stop at Dominick's tomorrow to get some cheap cereal, some milk for the girls, maybe some grapes, and some Johnsonville sausage.</p>\n\n<p>Maybe we won't grocery shop at all next week. Except, wait, my parents will be staying with us two nights. We might have to get just a few things, but I bet we could substract this week's overage from next weeks' budget.</p>\n")
        self.assert_(isinstance(b, mt.MoveableType))

    def testExtendedBodyFromAPI(self):
        """ Make sure we get extended body from api data """
        eb = mt.extendedbody(self.api_extendedbody)
        self.assertEqual(unicode(eb), 'Here is some more text.\n')
        self.assert_(isinstance(eb, mt.MoveableType))

    def testEmptyExtendedBodyFromTP(self):
        """ Make sure we get ValueError from the extended body of an empty typepad EXTENDED BODY:"""
        self.assertRaises(ValueError, mt.extendedbody, self.tp_extendedbody)

    def testEmtpyExcerptFromTP(self):
        """ Make sure we get ValueError from the excerpt of an empty typepad EXCERPT:"""
        self.assertRaises(ValueError, mt.excerpt, self.tp_excerpt)

    def testCommentsFromAPI(self):
        """ Make sure we have comments from api data """
        c1 = mt.comment(self.api_comment1)
        self.assertEqual(len(c1.keys()), 3)
        self.assert_('AUTHOR' in c1.keys())
        self.assertTrue(len(c1['AUTHOR']) > 0)
        self.assert_(isinstance(c1['BODY'], unicode))
        self.assertEqual(c1['BODY'], 'This is\nthe body of this comment.\n')
        c2 = mt.comment(self.api_comment2)
        self.assert_('AUTHOR' in c2.keys())
        self.assertTrue(len(c2['AUTHOR']) > 0)
        self.assertEqual(c2['BODY'], 'This is the body of\nanother comment. It goes\nup to here.\n')
        self.assert_(isinstance(c1, mt.MoveableType))
        self.assert_(isinstance(c2, mt.MoveableType))

    def testPingFromAPI(self):
        """ Make sure there is a ping object from api data """
        p = mt.ping(self.api_ping)
        self.assertEqual(len(p.keys()), 6)
        self.assert_('DATE' in p.keys())
        self.assertEqual(p['EXCERPT'], 'This is the start of my\nentry, and here it...\n')
        self.assert_(isinstance(p, mt.MoveableType))

    def testEntryFromAPI(self):
        """ Make sure there is a valid entry object from api data """
        e = mt.entry(self.api_entry)
        self.assert_(hasattr(e, 'metadata'))
        self.assert_(hasattr(e, 'body'))
        self.assert_(hasattr(e, 'extendedbody'))
        self.assert_(hasattr(e, 'comments'))
        self.assert_(hasattr(e, 'pings'))
        self.assertEqual(len(e.comments), 2)
        self.assertEqual(len(e.pings), 1)
        self.assert_(not hasattr(e, 'keywords'))
        self.assert_(not hasattr(e, 'excerpt'))
        self.assert_(isinstance(e, mt.MoveableType))

    def testEntryFromTP(self):
        """ Make sure there is a valid entry object from typepad data """
        e = mt.entry(self.tp_entry)
        self.assert_(hasattr(e, 'metadata'))
        self.assert_(hasattr(e, 'body'))
        self.assertEqual(e.extendedbody, None)
        self.assertEqual(e.excerpt, None)
        self.assertEqual(e.keywords, None)
        self.assert_(not hasattr(e, 'comments'))
        self.assert_(not hasattr(e, 'pings'))
        self.assert_(isinstance(e, mt.MoveableType))
        return

    def testBlogFromAPI(self):
        """ Make sure that every entry in api data converts to a blog entry """
        b = mt.blog(self.api_data)
        self.assertEqual(len(b), 2)
        self.assert_(isinstance(b, mt.MoveableType))

    def testBlogFromTP(self):
        """ Make sure that every entry in typepad data converts to a blog entry """
        b = mt.blog(self.tp_data)
        self.assertEqual(len(b), 53)
        self.assert_(isinstance(b, mt.MoveableType))


if __name__ == '__main__':
    unittest.main()