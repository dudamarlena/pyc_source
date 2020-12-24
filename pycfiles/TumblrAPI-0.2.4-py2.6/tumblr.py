# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/tumblr.py
# Compiled at: 2010-02-01 23:48:15
"""Tumblr API client

Pulls data about a Tumblr tumblelog into Python data structures 
using the Tumblr API.  Currently intended for reading but not writing.

See http://www.tumblr.com/api for API docs, such as they are.
"""
__version__ = '0.2.4'
__author__ = 'SNF Labs <jacob@spaceshipnofuture.org>'
__TODO__ = 'TODO List\n- Video: Parse the source and player fields\n- Audio\n- Quote: Parse a url out of Quote.source\n- Photo: Parse a url out of Photo.caption\n'
import urlparse, httplib2
try:
    import xml.etree.cElementTree as ElementTree
except:
    try:
        import xml.etree.ElementTree as ElementTree
    except:
        try:
            import cElementTree as ElementTree
        except:
            import ElementTree

USER_AGENT = 'Tumblr in the Bronx/%s +http://labs.spaceshipnofuture.org/tumblrapi/' % __version__
DEFAULT_HTTP_CACHE_DIR = '.cache'

class TumblrError(Exception):
    pass


class TumblrOhShitError(TumblrError):
    pass


class TumblrParseError(TumblrError):
    pass


class TumblrHTTPError(TumblrError):
    pass


class InternalServerError(TumblrHTTPError):
    pass


class ServiceUnavailableError(TumblrHTTPError):
    pass


class URLNotFoundError(TumblrHTTPError):
    pass


class URLForbiddenError(TumblrHTTPError):
    pass


class URLGoneError(TumblrHTTPError):
    pass


class UnsupportedContentTypeError(TumblrHTTPError):
    pass


class BadContentTypeError(TumblrHTTPError):
    pass


def _unicode(str):
    """A workaround for Python's built-in unicode().
    
    When unicode() is invoked against a variable with the value None, then unicode()
    will return u'None', which makes no sense to me.  
    
    It should return either None or u''.  This returns u''.
    """
    if str is None:
        return ''
    else:
        return unicode(str)
        return


def _isUrl(str):
    """Attempts to determine if the given string is really an HTTP URL.

    This is a quick-and-dirty test that just looks for an http protocol handler."""
    u = urlparse.urlparse(str)
    if u[0] == 'http' or u[0] == 'https':
        return True
    else:
        return False


class Feed(object):
    """A Feed object stores data relating to one of the Tumblelog's source feeds.
    
    Attributes:
    - id
    - url
    - type
    - title
    - next_update
    """

    def __init__(self, id, url, type, title, next_update):
        super(Feed, self).__init__()
        self.id = id
        self.url = url
        self.type = type
        self.title = title
        self.next_update = next_update


class Tumblelog(object):
    """Represents a single tumblelog.
    
    The TumbleLog object stores general metadata about the tumblelog, such as its name, 
    as well as the tumblelog's posts.
    
    Attributes:
    - http_response
    - name
    - cname
    - url
    - timezone
    - tagline
    - posts
    - num_posts
    - start
    - feeds
    """

    def __init__(self, logdata):
        super(Tumblelog, self).__init__()
        if logdata is None:
            raise TumblrOhShitError, 'Uh-oh'
        self.http_response = None
        self.title = _unicode(logdata.attrib.get('title'))
        self.name = _unicode(logdata.attrib.get('name'))
        self.cname = _unicode(logdata.attrib.get('cname'))
        if self.cname is None or self.cname == '':
            self.url = 'http://' + self.name + '.tumblr.com/'
        else:
            self.url = 'http://' + self.cname + '/'
        self.timezone = _unicode(logdata.attrib.get('timezone'))
        try:
            self.tagline = _unicode(logdata.text)
        except AttributeError:
            self.tagline = ''

        self.posts = []
        self.start = 0
        self.num_posts = 0
        self.feeds = {}
        try:
            for f in logdata.find('feeds').findall('feed'):
                id = int(f.attrib.get('id'))
                url = _unicode(f.attrib.get('url'))
                type = _unicode(f.attrib.get('import-type'))
                title = _unicode(f.attrib.get('title'))
                next_update = int(f.attrib.get('next-update-in-seconds'))
                self.feeds[id] = Feed(id, url, type, title, next_update)

        except AttributeError:
            self.feeds = None

        return


class Line(object):
    """A line in a conversation.
    
    Attributes:
    - name
    - label
    - content
    """

    def __init__(self, name, label, content):
        super(Line, self).__init__()
        self.name = name
        self.label = label
        self.content = content


class Post(object):
    """Generic Post object from which the others are derived.
    
    Attributes:
    - type
    - id
    - url
    - date_gmt
    - date
    - unixtime
    - source_feed
    - source_feed_id
    - source_url
    """

    def __init__(self, postdata):
        super(Post, self).__init__()
        self._keymap = {'permalink': 'url'}
        self.type = 'unknown'
        self.id = int(postdata.attrib.get('id'))
        self.url = _unicode(postdata.attrib.get('url'))
        self.date_gmt = _unicode(postdata.attrib.get('date-gmt'))
        self.date = _unicode(postdata.attrib.get('date'))
        self.unixtime = int(postdata.attrib.get('unix-timestamp'))
        try:
            self.source_feed_id = int(postdata.attrib.get('from-feed-id'))
            self.source_url = _unicode(postdata.attrib.get('feed-item'))
        except TypeError:
            self.source_feed_id = None
            self.source_url = None

        self.postdata = postdata
        return

    def __getattr__(self, attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            pass

        try:
            return self.__dict__[self._keymap[attr]]
        except:
            raise AttributeError, "object has no attribute '%s'" % attr


class Regular(Post):
    """A Regular freeform post.
    
    Attributes:
    - type
    - title
    - body/content/description
    
    See also the Post object.
    """

    def __init__(self, postdata):
        super(Regular, self).__init__(postdata)
        self.type = 'regular'
        try:
            self.title = _unicode(postdata.find('regular-title').text)
        except AttributeError:
            self.title = ''

        try:
            self.body = _unicode(postdata.find('regular-body').text)
        except AttributeError:
            self.body = ''

        self._keymap['content'] = 'body'
        self._keymap['description'] = 'body'


class Link(Post):
    """A Link, consisting of a title, url, and maybe a description.
    
    Attributes:
    - type
    - title
    - description/body/content
    - link_url/related
    
    See also the Post object.
    """

    def __init__(self, postdata):
        super(Link, self).__init__(postdata)
        self.type = 'link'
        try:
            self.title = _unicode(postdata.find('link-text').text)
        except AttributeError:
            self.title = ''

        try:
            self.description = _unicode(postdata.find('link-description').text)
        except AttributeError:
            self.description = ''

        try:
            self.link_url = _unicode(postdata.find('link-url').text)
        except AttributeError:
            self.link_url = ''

        self.via = ''
        self._keymap['body'] = 'description'
        self._keymap['content'] = 'description'
        self._keymap['related'] = 'link_url'


class Quote(Post):
    """A Quote and its source.
    
    Attributes:
    - type
    - quote/description/body/content
    - source
    """

    def __init__(self, postdata):
        super(Quote, self).__init__(postdata)
        self.type = 'quote'
        try:
            self.quote = _unicode(postdata.find('quote-text').text)
        except AttributeError:
            self.quote = ''

        try:
            self.source = _unicode(postdata.find('quote-source').text)
        except AttributeError:
            self.source = ''

        self._keymap['description'] = 'quote'
        self._keymap['body'] = 'quote'
        self._keymap['content'] = 'quote'


class Photo(Post):
    """A Photo, with a caption and several URLs of it in various sizes.
    
    Attributes:
    - type
    - caption/body/content/description
    - urls
    
    See also the Post object.
    """

    def __init__(self, postdata):
        super(Photo, self).__init__(postdata)
        self.type = 'photo'
        try:
            self.caption = _unicode(postdata.find('photo-caption').text)
        except AttributeError:
            self.caption = ''

        self.urls = {}
        for url in postdata.findall('photo-url'):
            self.urls[url.attrib.get('max-width')] = _unicode(url.text)

        self._keymap['body'] = 'caption'
        self._keymap['content'] = 'caption'
        self._keymap['description'] = 'caption'


class Conversation(Post):
    """A Conversation or chat log.  Each line is a Line object.
    
    Attributes:
    - type
    - description/body/content
    - lines
    
    See also the Post object.
    """

    def __init__(self, postdata):
        super(Conversation, self).__init__(postdata)
        self.type = 'conversation'
        self.description = postdata.find('conversation-text').text
        self.lines = []
        for line in postdata.findall('conversation-line'):
            name = _unicode(line.attrib.get('name'))
            label = _unicode(line.attrib.get('label'))
            content = _unicode(line.text)
            l = Line(name, label, content)
            self.lines.append(l)

        self._keymap['body'] = 'description'
        self._keymap['content'] = 'description'


class Video(Post):
    """A Video object.
    
    Attributes:
    - type
    - source
    - player
    - caption/body/content/description
    - title
    
    See also the Post object.
    """

    def __init__(self, postdata):
        super(Video, self).__init__(postdata)
        self.type = 'video'
        try:
            self.source = _unicode(postdata.find('video-source').text)
        except AttributeError:
            self.source = ''

        try:
            self.player = _unicode(postdata.find('video-player').text)
        except AttributeError:
            self.player = ''

        try:
            self.caption = _unicode(postdata.find('video-caption').text)
        except AttributeError:
            self.caption = ''

        self.title = ''
        self._keymap['body'] = 'caption'
        self._keymap['content'] = 'caption'
        self._keymap['description'] = 'caption'


class Audio(Post):
    """An Audio object.
    
    Attributes:
    - type
    - player
    - caption/content/body/description
    
    See also the Post object.
    """

    def __init__(self, postdata):
        super(Audio, self).__init__(postdata)
        self.type = 'audio'
        self.player = ''
        self.caption = ''
        self._keymap['body'] = 'caption'
        self._keymap['content'] = 'caption'
        self._keymap['description'] = 'caption'


def _parse_content_type(ct):
    """Given an HTTP content-type header, parses out the content-type and the charset.
    
    Does not currently perform any validation on the content of the header."""
    parts = ct.split(';')
    content_type = parts[0]
    try:
        charset = parts[1].strip().lstrip('charset=')
    except IndexError:
        charset = None

    return (
     content_type, charset)


def _fetch(url, cache_dir=DEFAULT_HTTP_CACHE_DIR, proxy_info=None):
    """Requests the Tumblr API URL and deals with any HTTP-related errors.
    
    Returns both an httplib2 Response object and the content."""
    valid_content_types = [
     'application/xml', 'text/xml']
    h = httplib2.Http(cache=cache_dir, proxy_info=proxy_info)
    try:
        (resp, content) = h.request(url, method='GET', headers={'User-Agent': USER_AGENT})
    except IOError:
        raise

    if resp.status == 403:
        raise URLForbiddenError
    if resp.status == 404:
        raise URLNotFoundError
    if resp.status == 410:
        raise URLGoneError
    if resp.status == 500:
        raise InternalServerError
    if resp.status == 503:
        raise ServiceUnavailableError
    (content_type, charset) = _parse_content_type(resp['content-type'])
    if content_type in valid_content_types:
        pass
    else:
        raise UnsupportedContentTypeError
    return (
     resp, content)


def _getTree(url_or_file, cache_dir=DEFAULT_HTTP_CACHE_DIR, proxy_info=None):
    """Fetches the Tumblr API XML and returns both the HTTP status and 
    an ElementTree representation of the content.
    
    Instead of a URL, this method also accepts an open file or a Tumblr
    XML string.  In those cases, the HTTP status is returned as None."""
    resp = None
    if isinstance(url_or_file, file):
        content = url_or_file.read()
    elif _isUrl(url_or_file):
        (resp, content) = _fetch(url_or_file, cache_dir, proxy_info)
    else:
        content = url_or_file
    try:
        tree = ElementTree.fromstring(content)
    except SyntaxError:
        raise TumblrParseError, 'SyntaxError while parsing XML!'

    return (
     resp, tree)


def parse(url_or_file, cache_dir=DEFAULT_HTTP_CACHE_DIR, proxy_info=None):
    """Parses Tumblr API XML into Python data structures.
    
    Accepts either a URL, an open file, or a hunk of XML in a string.
    """
    (resp, tree) = _getTree(url_or_file, cache_dir, proxy_info)
    tumblelog = Tumblelog(tree.find('tumblelog'))
    tumblelog.http_response = resp
    tumblelog.start = int(tree.find('posts').attrib.get('start'))
    tumblelog.num_posts = int(tree.find('posts').attrib.get('total'))
    posts = []
    for postdata in tree.find('posts'):
        type = postdata.attrib.get('type')
        if type == 'regular':
            post = Regular(postdata)
        elif type == 'link':
            post = Link(postdata)
        elif type == 'quote':
            post = Quote(postdata)
        elif type == 'photo':
            post = Photo(postdata)
        elif type == 'conversation':
            post = Conversation(postdata)
        elif type == 'video':
            post = Video(postdata)
        elif type == 'audio':
            post = Audio(postdata)
        else:
            post = Post(postdata)
        try:
            if post.source_feed_id:
                post.source_feed = tumblelog.feeds[post.source_feed_id]
        except KeyError:
            pass

        posts.append(post)

    tumblelog.posts = posts
    return tumblelog


def main():
    """Doesn't do anything currently; reserved for future use."""
    url = 'http://golden.cpl593h.net/api/read'


if __name__ == '__main__':
    main()