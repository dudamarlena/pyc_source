# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\typepad2blogger\blogger.py
# Compiled at: 2008-05-17 18:19:02
""" blogger - google blogger module 
    they have their own api, dammit
"""
__version__ = '0.0.1'
__all__ = ['BloggerError', 'Blogger', 'entry', 'comment', 'blog']
import gdata
from gdata import atom, service

class BloggerError(Exception):
    """ Error to throw when dealing with blogger """
    pass


class Blogger(object):
    """ Base class so we can ask if object is a MoveableType object """
    pass


class entry(Blogger, gdata.GDataEntry):
    """ a blogger entry object """

    def __init__(self, title, body, author, publishdate):
        gdata.GDataEntry.__init__(self)
        self.author.append(atom.Author(atom.Name(text=author)))
        self.title = atom.Title(title_type='xhtml', text=title)
        self.content = atom.Content(content_type='html', text=body)
        self.published = atom.Published(text=publishdate)


class comment(Blogger, gdata.GDataEntry):
    """ a blogger comment object
    We're still missing everything in an MT post,
    except for the BODY. 
    * AUTHOR
    * EMAIL
    * URL
    * IP
    * DATE
    * BODY
    """

    def __init__(self, body, publishdate):
        gdata.GDataEntry.__init__(self)
        self.content = atom.Content(content_type='xhtml', text=body)
        self.published = atom.Published(text=publishdate)


class blog(Blogger):

    def __init__(self, email=None, password=None, title=None):
        self.connected = False
        if email:
            self.email = email
        if password:
            self.password = password
        if title:
            self.title = title
        if self.email and self.password and self.title:
            self.connection = service.GDataService(self.email, self.password)
            self.connection.source = str(type(self))[8:-2].replace('.', '_') + '-' + __version__
            self.connection.service = 'blogger'
            self.connection.server = 'www.blogger.com'
        else:
            self.connection = None
        return

    def connect(self, email=None, password=None, title=None):
        self.__init__(email or self.email, password or self.password, title or self.title)
        try:
            self.connection.ProgrammaticLogin()
            self.connected = True
        except Exception, e:
            raise e

        self.feed = self.connection.Get('/feeds/default/blogs')
        for entry in self.feed.entry:
            if entry.title.text.lower() == self.title.lower():
                self.link = entry.GetSelfLink()
                self.id = self.link.href.split('/')[(-1)]
                self.__GDataEntry = entry
                break

        if not hasattr(self, 'id'):
            raise BloggerError("No blog named '%s'" % self.title)

    def post(self, entry, draft=True):
        """ post entry to blogger
        
        This is lifted from BloggerExample.py 
        included with the py gdata api.
        
        If the insertion is successful, the added post (GDataEntry) will be returned.
        """
        if draft:
            control = atom.Control()
            control.draft = atom.Draft(text='yes')
            entry.control = control
        if not self.connected:
            self.connect()
        return self.connection.Post(entry, '/feeds/' + self.id + '/posts/default')