# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tweetworks/User.py
# Compiled at: 2009-07-04 21:33:26
"""
Read Tweetworks API users from XML responses.

Nicolas Ward
@ultranurd
ultranurd@yahoo.com
http://www.ultranurd.net/code/tweetworks/
2009.06.19
"""
import lxml.etree
from lxml.builder import E

class User:
    """
    Represents the data fields of a single Tweetworks user.
    """

    def __init__(self, xml=None):
        """
        Reads user fields from the XML, or create an empty user.

        id - int - Tweetworks numeric user ID
        username - string - Tweetworks/Twitter username
        avatar_url - string - Twitter avatar URL
        twitter_id - int - Twitter numeric user ID
        """
        if xml == None:
            self.id = None
            self.username = ''
            self.avatar_url = ''
            self.twitter_id = None
            return
        else:
            self.id = int(xml.xpath('/user/id/text()')[0])
            self.username = unicode(xml.xpath('/user/username/text()')[0])
            self.avatar_url = unicode(xml.xpath('/user/avatar_url/text()')[0])
            self.name = unicode(xml.xpath('/user/name/text()')[0])
            twitter_id = xml.xpath('/user/twitter_id/text()')
            if len(twitter_id) == 1:
                self.twitter_id = int(twitter_id[0])
            else:
                self.twitter_id = None
            return

    def __str__(self):
        """
        Returns this User as an XML string.
        """
        return lxml.etree.tostring(self.xml())

    def __repr__(self):
        """
        Returns an eval-ready string for this User's constructor.
        """
        return 'tweetworks.User(lxml.etree.parsestring(%s))' % repr(str(self))

    def xml(self):
        """
        Generates an XML element tree for this User.
        """
        xml = E('user', E('id', str(self.id)), E('username', self.username), E('avatar_url', self.avatar_url), E('name', self.name), E('twitter_id', (
         '', str(self.twitter_id))[(self.twitter_id != None)]))
        return xml