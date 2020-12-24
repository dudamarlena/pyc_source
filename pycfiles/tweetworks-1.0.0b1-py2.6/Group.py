# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tweetworks/Group.py
# Compiled at: 2009-07-04 21:39:49
"""
Read Tweetworks API groups from XML responses.

Nicolas Ward
@ultranurd
ultranurd@yahoo.com
http://www.ultranurd.net/code/tweetworks/
2009.06.19
"""
import lxml.etree
from lxml.builder import E

class Group:
    """
    Represents the data fields of a single Tweetworks group.
    """

    def __init__(self, xml=None):
        """
        Reads group fields from the XML, or create an empty group.

        id - int - Tweetworks numeric group ID
        name - string - Tweetworks group name
        private - boolean - Whether or not this is a private group
        description - string - The short group description, if any
        """
        if xml == None:
            self.id = None
            self.name = ''
            self.private = False
            self.description = ''
            return
        else:
            self.id = int(xml.xpath('/group/id/text()')[0])
            self.name = unicode(xml.xpath('/group/name/text()')[0])
            private = xml.xpath('/group/private/text()')
            if len(private) == 1 and private[0] == '1':
                self.private = True
            else:
                self.private = False
            description = xml.xpath('/group/description/text()')
            if len(description) == 1:
                self.description = unicode(description[0])
            else:
                self.description = ''
            return

    def __str__(self):
        """
        Returns this Group as an XML string.
        """
        return lxml.etree.tostring(self.xml())

    def __repr__(self):
        """
        Returns an eval-ready string for this Group's constructor.
        """
        return 'tweetworks.Group(lxml.etree.parsestring(%s))' % repr(str(self))

    def xml(self):
        """
        Generates an XML element tree for this Group.
        """
        xml = E('group', E('id', str(self.id)), E('name', self.name), (
         E('private'), E('private', '1'))[self.private])
        if self.description != '':
            xml.append(E('description', self.description))
        return xml