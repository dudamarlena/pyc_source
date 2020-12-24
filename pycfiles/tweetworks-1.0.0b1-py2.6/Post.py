# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tweetworks/Post.py
# Compiled at: 2009-07-04 21:37:32
"""
Read Tweetworks API posts from XML responses.

Nicolas Ward
@ultranurd
ultranurd@yahoo.com
http://www.ultranurd.net/code/tweetworks/
2009.06.19
"""
import iso8601, lxml.etree
from lxml.builder import E
import tweetworks

class Post:
    """
    Represents the data fields of a single Tweetworks post.
    """

    def __init__(self, xml=None):
        """
        Reads post fields from the XML, or create an empty post.

        id - int - Tweetworks numeric post ID
        user_id - int - Tweetworks numeric user ID of poster
        group_id - int - Tweetworks numeric ID of containing group, if any
        parent_id - int - Tweetworks numeric ID of parent post, if any
        twitter_id - int - Twitter numeric ID of post, if cross-posted
        bingo - boolean - Whether this post has been marked as a bingo
        body - string - The contents of this post
        created - datetime - When this post was created on Tweetworks
        group - tweetworks.Group - Object representing containing group, if any
        user - tweetworks.User - Object representing poster
        replies - int - The number of replies to this post, if any
        posts - tweetworks.Post[] - The Post object replies to this post, if any
        """
        if xml == None:
            self.id = None
            self.user_id = None
            self.group_id = None
            self.parent_id = None
            self.twitter_id = None
            self.bingo = False
            self.body = ''
            self.created = datetime.datetime.now()
            self.group = None
            self.user = None
            self.replies = 0
            self.posts = []
            return
        else:
            self.id = int(xml.xpath('/post/id/text()')[0])
            self.user_id = int(xml.xpath('/post/user_id/text()')[0])
            group_id = xml.xpath('/post/group_id/text()')
            if len(group_id) == 1:
                self.group_id = int(group_id[0])
            else:
                self.group_id = None
            parent_id = xml.xpath('/post/parent_id/text()')
            if len(parent_id) == 1:
                self.parent_id = int(parent_id[0])
            else:
                self.parent_id = None
            twitter_id = xml.xpath('/post/twitter_id/text()')
            if len(twitter_id) == 1:
                self.twitter_id = int(twitter_id[0])
            else:
                self.twitter_id = None
            bingo = xml.xpath('/post/bingo/text()')
            if len(bingo) == 1 and bingo[0] == '1':
                self.bingo = True
            else:
                self.bingo = False
            self.body = unicode(xml.xpath('/post/body/text()')[0])
            self.created = iso8601.parse_date(xml.xpath('/post/created/text()')[0])
            replies = xml.xpath('/post/replies/text()')
            if len(replies) == 1:
                self.replies = int(replies[0])
            else:
                self.replies = 0
            if self.group_id != None:
                group_string = lxml.etree.tostring(xml.xpath('/post/group')[0])
                self.group = tweetworks.Group(lxml.etree.fromstring(group_string))
            else:
                self.group = None
            user_string = lxml.etree.tostring(xml.xpath('/post/user')[0])
            self.user = tweetworks.User(lxml.etree.fromstring(user_string))
            self.posts = []
            for post_xml in xml.xpath('/post/posts/post[node()]'):
                post_string = lxml.etree.tostring(post_xml)
                self.posts.append(Post(lxml.etree.fromstring(post_string)))

            return

    def __str__(self):
        """
        Returns this Post as an XML string.
        """
        return lxml.etree.tostring(self.xml())

    def __repr__(self):
        """
        Returns an eval-ready string for this Post's constructor.
        """
        return 'tweetworks.Post(lxml.etree.parsestring(%s))' % repr(str(self))

    def xml(self):
        """
        Generates an XML element tree for this Post.
        """
        xml = E('post', E('id', str(self.id)), E('user_id', str(self.user_id)), (
         E('group_id'),
         E('group_id', str(self.group_id)))[(self.group_id != None)], (
         E('parent_id'),
         E('parent_id', str(self.parent_id)))[(self.parent_id != None)], (
         E('twitter_id'),
         E('twitter_id', str(self.twitter_id)))[(self.twitter_id != None)], (
         E('bingo'), E('bingo', '1'))[self.bingo], E('body', self.body), E('created', str(self.created).replace(' ', 'T')), E('replies', str(self.replies)))
        if self.group == None:
            xml.append(E('group', E('id'), E('name'), E('private')))
        else:
            xml.append(self.group.xml())
        if self.user == None:
            xml.append(E('user'))
        else:
            xml.append(self.user.xml())
        if len(self.posts) > 0:
            posts_xml = E('posts', *[ post.xml() for post in self.posts ])
            xml.append(posts_xml)
        else:
            xml.append(E('posts', E('post')))
        return xml