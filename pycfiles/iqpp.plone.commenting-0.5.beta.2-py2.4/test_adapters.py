# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/tests/test_adapters.py
# Compiled at: 2007-10-07 06:52:18
from base import CommentingTestCase
from iqpp.plone.commenting.interfaces import ICommenting

class TestCommentManagement(CommentingTestCase):
    __module__ = __name__

    def testAddComment_1(self):
        manager = ICommenting(self.d)
        new_comment = manager.addComment(reply_to='', subject='My Subject', message='My Message', name='John Doe')
        comments = manager.getAllComments()
        self.assertEqual(len(comments), 1)
        comments = manager.getComments()
        self.assertEqual(len(comments), 1)
        comment = comments[0]
        self.assertEqual(comment.id, new_comment.id)
        self.assertEqual(comment.reply_to, '')
        self.assertEqual(comment.subject, 'My Subject')
        self.assertEqual(comment.message, 'My Message')
        self.assertEqual(comment.name, 'John Doe')
        comments = manager.getComments(new_comment.id)
        self.assertEqual(len(comments), 0)
        comment = manager.getComment(new_comment.id)
        self.assertEqual(comment.id, new_comment.id)
        self.assertEqual(comment.reply_to, '')
        self.assertEqual(comment.subject, 'My Subject')
        self.assertEqual(comment.message, 'My Message')
        self.assertEqual(comment.name, 'John Doe')

    def testAddComment_2(self):
        """Add an comment with german umlauts as strings.
        """
        manager = ICommenting(self.d)
        new_comment = manager.addComment(reply_to='', subject='öäüÖÄÜß', message='öäüÖÄÜß', name='öäüÖÄÜß')
        comment = manager.getComment(new_comment.id)
        self.assertEqual(comment.id, new_comment.id)
        self.assertEqual(comment.reply_to, '')
        self.assertEqual(comment.subject, 'Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f')
        self.assertEqual(comment.message, 'Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f')
        self.assertEqual(comment.name, 'Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f')

    def testAddComment_2(self):
        """Add an comment with german umlauts as unicode.
        """
        manager = ICommenting(self.d)
        new_comment = manager.addComment(reply_to='', subject='Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f', message='Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f', name='Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f')
        comment = manager.getComment(new_comment.id)
        self.assertEqual(comment.id, new_comment.id)
        self.assertEqual(comment.reply_to, '')
        self.assertEqual(comment.subject, 'Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f')
        self.assertEqual(comment.message, 'Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f')
        self.assertEqual(comment.name, 'Ã¶Ã¤Ã¼Ã\x96Ã\x84Ã\x9cÃ\x9f')

    def testAddCommentOfComment(self):
        manager = ICommenting(self.d)
        comment = manager.addComment(reply_to='', subject='My Subject', message='My Message', name='John Doe')
        reply = manager.addComment(reply_to=comment.id, subject='My Reply', message='My Reply Message', name='Jane Doe')
        comments = manager.getAllComments()
        self.assertEqual(len(comments), 2)
        comments = manager.getComments()
        self.assertEqual(len(comments), 1)
        comments = manager.getComments(comment.id)
        self.assertEqual(len(comments), 1)
        comments = manager.getComments(reply.id)
        self.assertEqual(len(comments), 0)

    def testDeleteComment1(self):
        """
        """
        manager = ICommenting(self.d)
        comment_1 = manager.addComment(reply_to='', subject='My Comment 1', message='My Message 1', name='John Doe')
        reply_id = manager.addComment(reply_to=comment_1.id, subject='My Reply', message='My Reply Message', name='Jane Doe')
        comment_2 = manager.addComment(reply_to='', subject='My Comment 2', message='My Message 2', name='John Doe')
        comments = manager.getAllComments()
        self.assertEqual(len(comments), 3)
        manager.deleteComment(comment_1.id)
        comments = manager.getAllComments()
        self.assertEqual(len(comments), 1)

    def testDeleteReply(self):
        """
        """
        manager = ICommenting(self.d)
        comment_1 = manager.addComment(reply_to='', subject='My Comment 1', message='My Message 1', name='John Doe')
        reply = manager.addComment(reply_to=comment_1.id, subject='My Reply', message='My Reply Message', name='Jane Doe')
        comment_2 = manager.addComment(reply_to='', subject='My Comment 2', message='My Message 2', name='John Doe')
        comments = manager.getAllComments()
        self.assertEqual(len(comments), 3)
        manager.deleteComment(reply.id)
        comments = manager.getAllComments()
        self.assertEqual(len(comments), 2)

    def testDeleteComments(self):
        """
        """
        manager = ICommenting(self.d)
        comment_1 = manager.addComment(reply_to='', subject='My Comment 1', message='My Message 1', name='John Doe')
        reply_id = manager.addComment(reply_to=comment_1.id, subject='My Reply', message='My Reply Message', name='Jane Doe')
        comment_2 = manager.addComment(reply_to='', subject='My Comment 2', message='My Message 2', name='John Doe')
        manager.deleteComments()
        comments = manager.getAllComments()
        self.assertEqual(len(comments), 0)

    def testEditComment(self):
        """
        """
        manager = ICommenting(self.d)
        comment_1 = manager.addComment(reply_to='', subject='My Comment 1', message='My Message 1', name='John Doe')
        manager.manageComment(comment_id=comment_1.id, reply_to='', subject='Modified Subject', message='Modified Message', name='Jane Doe', member_id='', email='', review_state='published')
        comment = manager.getComment(comment_1.id)
        self.assertEqual(comment.id, comment_1.id)
        self.assertEqual(comment.reply_to, '')
        self.assertEqual(comment.subject, 'Modified Subject')
        self.assertEqual(comment.message, 'Modified Message')
        self.assertEqual(comment.name, 'Jane Doe')
        self.assertEqual(comment.review_state, 'published')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCommentManagement))
    return suite