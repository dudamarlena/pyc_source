# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/tests/test_options.py
# Compiled at: 2007-10-07 06:52:18
from base import CommentingTestCase
from iqpp.plone.commenting.interfaces import ICommenting
from iqpp.plone.commenting.interfaces import ICommentingOptions
from iqpp.plone.commenting.interfaces import IGlobalCommenting

class TestModeration(CommentingTestCase):
    __module__ = __name__

    def testAddCommentViaAdapter(self):
        manager = ICommenting(self.d)
        new_id = manager.addComment(reply_to='', subject='My Subject', message='My Message', name='John Doe')
        adapter = IGlobalCommenting(self.d)
        pending_comments = adapter.getPendingComments()
        self.assertEqual(new_id.id, pending_comments[0]['comment_id'])
        self.assertEqual(self.d.absolute_url(), pending_comments[0]['object_url'])
        self.assertEqual(1, len(pending_comments))

    def testAddCommentViaView(self):
        c = ICommenting(self.d)
        new_id = c.addComment(reply_to='', subject='My Subject', message='My Message', name='John Doe')
        gc = IGlobalCommenting(self.d)
        pending_comments = gc.getPendingComments()
        self.assertEqual(new_id.id, pending_comments[0]['comment_id'])
        self.assertEqual(self.d.absolute_url(), pending_comments[0]['object_url'])
        self.assertEqual(1, len(pending_comments))


class TestOptions(CommentingTestCase):
    """tests the setting and retrieval of the options of a commentable."""
    __module__ = __name__

    def testMailFrom(self):
        options1 = ICommentingOptions(self.d)
        options2 = ICommentingOptions(self.d2)
        self.assertEqual(options1.mail_from, ICommentingOptions.get('mail_from').default)
        self.assertEqual(options2.mail_from, ICommentingOptions.get('mail_from').default)
        options1.mail_from = 'john@doe.com'
        self.assertEqual(options1.mail_from, 'john@doe.com')
        self.assertEqual(options2.mail_from, ICommentingOptions.get('mail_from').default)

    def testMailTo(self):
        options1 = ICommentingOptions(self.d)
        options2 = ICommentingOptions(self.d2)
        self.assertEqual(options1.mail_to, ICommentingOptions.get('mail_to').default)
        self.assertEqual(options2.mail_to, ICommentingOptions.get('mail_to').default)
        options1.mail_to = 'john@doe.com'
        self.assertEqual(options1.mail_to, 'john@doe.com')
        self.assertEqual(options2.mail_to, ICommentingOptions.get('mail_to').default)

    def testModerationFlag(self):
        options1 = ICommentingOptions(self.d)
        options2 = ICommentingOptions(self.d2)
        self.assertEqual(options1.is_moderated, ICommentingOptions.get('is_moderated').default)
        self.assertEqual(options2.is_moderated, ICommentingOptions.get('is_moderated').default)
        options1.is_moderated = False
        self.assertEqual(options1.is_moderated, False)
        self.assertEqual(options2.is_moderated, ICommentingOptions.get('is_moderated').default)
        options1.is_moderated = True
        self.assertEqual(options1.is_moderated, True)
        self.assertEqual(options2.is_moderated, ICommentingOptions.get('is_moderated').default)

    def testPreviewFlag(self):
        options1 = ICommentingOptions(self.d)
        options2 = ICommentingOptions(self.d2)
        self.assertEqual(options1.show_preview, ICommentingOptions.get('show_preview').default)
        self.assertEqual(options2.show_preview, ICommentingOptions.get('show_preview').default)
        options1.show_preview = False
        self.assertEqual(options1.show_preview, False)
        self.assertEqual(options2.show_preview, ICommentingOptions.get('show_preview').default)
        options1.show_preview = True
        self.assertEqual(options1.show_preview, True)
        self.assertEqual(options2.show_preview, ICommentingOptions.get('show_preview').default)

    def testSendCommentAddedMailFlag(self):
        options1 = ICommentingOptions(self.d)
        options2 = ICommentingOptions(self.d2)
        self.assertEqual(options1.send_comment_added_mail, ICommentingOptions.get('send_comment_added_mail').default)
        self.assertEqual(options2.send_comment_added_mail, ICommentingOptions.get('send_comment_added_mail').default)
        options1.send_comment_added_mail = False
        self.assertEqual(options1.send_comment_added_mail, False)
        self.assertEqual(options2.send_comment_added_mail, ICommentingOptions.get('send_comment_added_mail').default)
        options1.send_comment_added_mail = True
        self.assertEqual(options1.send_comment_added_mail, True)
        self.assertEqual(options2.send_comment_added_mail, ICommentingOptions.get('send_comment_added_mail').default)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestModeration))
    suite.addTest(makeSuite(TestOptions))
    return suite