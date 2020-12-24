# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/feedgenerator.py
# Compiled at: 2019-02-14 00:35:17
"""
Syndication feed generation library -- used for generating RSS, etc.

Sample usage:

>>> from django.utils import feedgenerator
>>> feed = feedgenerator.Rss201rev2Feed(
...     title="Poynter E-Media Tidbits",
...     link="http://www.poynter.org/column.asp?id=31",
...     description="A group Weblog by the sharpest minds in online media/journalism/publishing.",
...     language="en",
... )
>>> feed.add_item(
...     title="Hello",
...     link="http://www.holovaty.com/test/",
...     description="Testing."
... )
>>> with open('test.rss', 'w') as fp:
...     feed.write(fp, 'utf-8')

For definitions of the different versions of RSS, see:
http://web.archive.org/web/20110718035220/http://diveintomark.org/archives/2004/02/04/incompatible-rss
"""
from __future__ import unicode_literals
import datetime, warnings
from django.utils import datetime_safe, six
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text, iri_to_uri
from django.utils.six import StringIO
from django.utils.six.moves.urllib.parse import urlparse
from django.utils.timezone import utc
from django.utils.xmlutils import SimplerXMLGenerator

def rfc2822_date(date):
    months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
              'Nov', 'Dec')
    days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    date = datetime_safe.new_datetime(date)
    dow = days[date.weekday()]
    month = months[(date.month - 1)]
    time_str = date.strftime(b'%s, %%d %s %%Y %%H:%%M:%%S ' % (dow, month))
    if six.PY2:
        time_str = time_str.decode(b'utf-8')
    offset = date.utcoffset()
    if offset is None:
        return time_str + b'-0000'
    else:
        timezone = offset.days * 24 * 60 + offset.seconds // 60
        hour, minute = divmod(timezone, 60)
        return time_str + b'%+03d%02d' % (hour, minute)
        return


def rfc3339_date(date):
    date = datetime_safe.new_datetime(date)
    time_str = date.strftime(b'%Y-%m-%dT%H:%M:%S')
    if six.PY2:
        time_str = time_str.decode(b'utf-8')
    offset = date.utcoffset()
    if offset is None:
        return time_str + b'Z'
    else:
        timezone = offset.days * 24 * 60 + offset.seconds // 60
        hour, minute = divmod(timezone, 60)
        return time_str + b'%+03d:%02d' % (hour, minute)
        return


def get_tag_uri(url, date):
    """
    Creates a TagURI.

    See http://web.archive.org/web/20110514113830/http://diveintomark.org/archives/2004/05/28/howto-atom-id
    """
    bits = urlparse(url)
    d = b''
    if date is not None:
        d = b',%s' % datetime_safe.new_datetime(date).strftime(b'%Y-%m-%d')
    return b'tag:%s%s:%s/%s' % (bits.hostname, d, bits.path, bits.fragment)


class SyndicationFeed(object):
    """Base class for all syndication feeds. Subclasses should provide write()"""

    def __init__(self, title, link, description, language=None, author_email=None, author_name=None, author_link=None, subtitle=None, categories=None, feed_url=None, feed_copyright=None, feed_guid=None, ttl=None, **kwargs):

        def to_unicode(s):
            return force_text(s, strings_only=True)

        if categories:
            categories = [ force_text(c) for c in categories ]
        if ttl is not None:
            ttl = force_text(ttl)
        self.feed = {b'title': to_unicode(title), b'link': iri_to_uri(link), 
           b'description': to_unicode(description), 
           b'language': to_unicode(language), 
           b'author_email': to_unicode(author_email), 
           b'author_name': to_unicode(author_name), 
           b'author_link': iri_to_uri(author_link), 
           b'subtitle': to_unicode(subtitle), 
           b'categories': categories or (), 
           b'feed_url': iri_to_uri(feed_url), 
           b'feed_copyright': to_unicode(feed_copyright), 
           b'id': feed_guid or link, 
           b'ttl': ttl}
        self.feed.update(kwargs)
        self.items = []
        return

    def add_item(self, title, link, description, author_email=None, author_name=None, author_link=None, pubdate=None, comments=None, unique_id=None, unique_id_is_permalink=None, enclosure=None, categories=(), item_copyright=None, ttl=None, updateddate=None, enclosures=None, **kwargs):
        """
        Adds an item to the feed. All args are expected to be Python Unicode
        objects except pubdate and updateddate, which are datetime.datetime
        objects, and enclosures, which is an iterable of instances of the
        Enclosure class.
        """

        def to_unicode(s):
            return force_text(s, strings_only=True)

        if categories:
            categories = [ to_unicode(c) for c in categories ]
        if ttl is not None:
            ttl = force_text(ttl)
        if enclosure is None:
            enclosures = [] if enclosures is None else enclosures
        else:
            warnings.warn(b'The enclosure keyword argument is deprecated, use enclosures instead.', RemovedInDjango20Warning, stacklevel=2)
            enclosures = [
             enclosure]
        item = {b'title': to_unicode(title), b'link': iri_to_uri(link), 
           b'description': to_unicode(description), 
           b'author_email': to_unicode(author_email), 
           b'author_name': to_unicode(author_name), 
           b'author_link': iri_to_uri(author_link), 
           b'pubdate': pubdate, 
           b'updateddate': updateddate, 
           b'comments': to_unicode(comments), 
           b'unique_id': to_unicode(unique_id), 
           b'unique_id_is_permalink': unique_id_is_permalink, 
           b'enclosures': enclosures, 
           b'categories': categories or (), 
           b'item_copyright': to_unicode(item_copyright), 
           b'ttl': ttl}
        item.update(kwargs)
        self.items.append(item)
        return

    def num_items(self):
        return len(self.items)

    def root_attributes(self):
        """
        Return extra attributes to place on the root (i.e. feed/channel) element.
        Called from write().
        """
        return {}

    def add_root_elements(self, handler):
        """
        Add elements in the root (i.e. feed/channel) element. Called
        from write().
        """
        pass

    def item_attributes(self, item):
        """
        Return extra attributes to place on each item (i.e. item/entry) element.
        """
        return {}

    def add_item_elements(self, handler, item):
        """
        Add elements on each item (i.e. item/entry) element.
        """
        pass

    def write(self, outfile, encoding):
        """
        Outputs the feed in the given encoding to outfile, which is a file-like
        object. Subclasses should override this.
        """
        raise NotImplementedError(b'subclasses of SyndicationFeed must provide a write() method')

    def writeString(self, encoding):
        """
        Returns the feed in the given encoding as a string.
        """
        s = StringIO()
        self.write(s, encoding)
        return s.getvalue()

    def latest_post_date(self):
        """
        Returns the latest item's pubdate or updateddate. If no items
        have either of these attributes this returns the current UTC date/time.
        """
        latest_date = None
        date_keys = ('updateddate', 'pubdate')
        for item in self.items:
            for date_key in date_keys:
                item_date = item.get(date_key)
                if item_date:
                    if latest_date is None or item_date > latest_date:
                        latest_date = item_date

        return latest_date or datetime.datetime.utcnow().replace(tzinfo=utc)


class Enclosure(object):
    """Represents an RSS enclosure"""

    def __init__(self, url, length, mime_type):
        """All args are expected to be Python Unicode objects"""
        self.length, self.mime_type = length, mime_type
        self.url = iri_to_uri(url)


class RssFeed(SyndicationFeed):
    content_type = b'application/rss+xml; charset=utf-8'

    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement(b'rss', self.rss_attributes())
        handler.startElement(b'channel', self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement(b'rss')

    def rss_attributes(self):
        return {b'version': self._version, b'xmlns:atom': b'http://www.w3.org/2005/Atom'}

    def write_items(self, handler):
        for item in self.items:
            handler.startElement(b'item', self.item_attributes(item))
            self.add_item_elements(handler, item)
            handler.endElement(b'item')

    def add_root_elements(self, handler):
        handler.addQuickElement(b'title', self.feed[b'title'])
        handler.addQuickElement(b'link', self.feed[b'link'])
        handler.addQuickElement(b'description', self.feed[b'description'])
        if self.feed[b'feed_url'] is not None:
            handler.addQuickElement(b'atom:link', None, {b'rel': b'self', b'href': self.feed[b'feed_url']})
        if self.feed[b'language'] is not None:
            handler.addQuickElement(b'language', self.feed[b'language'])
        for cat in self.feed[b'categories']:
            handler.addQuickElement(b'category', cat)

        if self.feed[b'feed_copyright'] is not None:
            handler.addQuickElement(b'copyright', self.feed[b'feed_copyright'])
        handler.addQuickElement(b'lastBuildDate', rfc2822_date(self.latest_post_date()))
        if self.feed[b'ttl'] is not None:
            handler.addQuickElement(b'ttl', self.feed[b'ttl'])
        return

    def endChannelElement(self, handler):
        handler.endElement(b'channel')

    @property
    def mime_type(self):
        warnings.warn(b'The mime_type attribute of RssFeed is deprecated. Use content_type instead.', RemovedInDjango20Warning, stacklevel=2)
        return self.content_type


class RssUserland091Feed(RssFeed):
    _version = b'0.91'

    def add_item_elements(self, handler, item):
        handler.addQuickElement(b'title', item[b'title'])
        handler.addQuickElement(b'link', item[b'link'])
        if item[b'description'] is not None:
            handler.addQuickElement(b'description', item[b'description'])
        return


class Rss201rev2Feed(RssFeed):
    _version = b'2.0'

    def add_item_elements(self, handler, item):
        handler.addQuickElement(b'title', item[b'title'])
        handler.addQuickElement(b'link', item[b'link'])
        if item[b'description'] is not None:
            handler.addQuickElement(b'description', item[b'description'])
        if item[b'author_name'] and item[b'author_email']:
            handler.addQuickElement(b'author', b'%s (%s)' % (item[b'author_email'], item[b'author_name']))
        else:
            if item[b'author_email']:
                handler.addQuickElement(b'author', item[b'author_email'])
            elif item[b'author_name']:
                handler.addQuickElement(b'dc:creator', item[b'author_name'], {b'xmlns:dc': b'http://purl.org/dc/elements/1.1/'})
            if item[b'pubdate'] is not None:
                handler.addQuickElement(b'pubDate', rfc2822_date(item[b'pubdate']))
            if item[b'comments'] is not None:
                handler.addQuickElement(b'comments', item[b'comments'])
            if item[b'unique_id'] is not None:
                guid_attrs = {}
                if isinstance(item.get(b'unique_id_is_permalink'), bool):
                    guid_attrs[b'isPermaLink'] = str(item[b'unique_id_is_permalink']).lower()
                handler.addQuickElement(b'guid', item[b'unique_id'], guid_attrs)
            if item[b'ttl'] is not None:
                handler.addQuickElement(b'ttl', item[b'ttl'])
            if item[b'enclosures']:
                enclosures = list(item[b'enclosures'])
                if len(enclosures) > 1:
                    raise ValueError(b'RSS feed items may only have one enclosure, see http://www.rssboard.org/rss-profile#element-channel-item-enclosure')
                enclosure = enclosures[0]
                handler.addQuickElement(b'enclosure', b'', {b'url': enclosure.url, 
                   b'length': enclosure.length, 
                   b'type': enclosure.mime_type})
            for cat in item[b'categories']:
                handler.addQuickElement(b'category', cat)

        return


class Atom1Feed(SyndicationFeed):
    content_type = b'application/atom+xml; charset=utf-8'
    ns = b'http://www.w3.org/2005/Atom'

    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement(b'feed', self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        handler.endElement(b'feed')

    def root_attributes(self):
        if self.feed[b'language'] is not None:
            return {b'xmlns': self.ns, b'xml:lang': self.feed[b'language']}
        else:
            return {b'xmlns': self.ns}
            return

    def add_root_elements(self, handler):
        handler.addQuickElement(b'title', self.feed[b'title'])
        handler.addQuickElement(b'link', b'', {b'rel': b'alternate', b'href': self.feed[b'link']})
        if self.feed[b'feed_url'] is not None:
            handler.addQuickElement(b'link', b'', {b'rel': b'self', b'href': self.feed[b'feed_url']})
        handler.addQuickElement(b'id', self.feed[b'id'])
        handler.addQuickElement(b'updated', rfc3339_date(self.latest_post_date()))
        if self.feed[b'author_name'] is not None:
            handler.startElement(b'author', {})
            handler.addQuickElement(b'name', self.feed[b'author_name'])
            if self.feed[b'author_email'] is not None:
                handler.addQuickElement(b'email', self.feed[b'author_email'])
            if self.feed[b'author_link'] is not None:
                handler.addQuickElement(b'uri', self.feed[b'author_link'])
            handler.endElement(b'author')
        if self.feed[b'subtitle'] is not None:
            handler.addQuickElement(b'subtitle', self.feed[b'subtitle'])
        for cat in self.feed[b'categories']:
            handler.addQuickElement(b'category', b'', {b'term': cat})

        if self.feed[b'feed_copyright'] is not None:
            handler.addQuickElement(b'rights', self.feed[b'feed_copyright'])
        return

    def write_items(self, handler):
        for item in self.items:
            handler.startElement(b'entry', self.item_attributes(item))
            self.add_item_elements(handler, item)
            handler.endElement(b'entry')

    def add_item_elements(self, handler, item):
        handler.addQuickElement(b'title', item[b'title'])
        handler.addQuickElement(b'link', b'', {b'href': item[b'link'], b'rel': b'alternate'})
        if item[b'pubdate'] is not None:
            handler.addQuickElement(b'published', rfc3339_date(item[b'pubdate']))
        if item[b'updateddate'] is not None:
            handler.addQuickElement(b'updated', rfc3339_date(item[b'updateddate']))
        if item[b'author_name'] is not None:
            handler.startElement(b'author', {})
            handler.addQuickElement(b'name', item[b'author_name'])
            if item[b'author_email'] is not None:
                handler.addQuickElement(b'email', item[b'author_email'])
            if item[b'author_link'] is not None:
                handler.addQuickElement(b'uri', item[b'author_link'])
            handler.endElement(b'author')
        if item[b'unique_id'] is not None:
            unique_id = item[b'unique_id']
        else:
            unique_id = get_tag_uri(item[b'link'], item[b'pubdate'])
        handler.addQuickElement(b'id', unique_id)
        if item[b'description'] is not None:
            handler.addQuickElement(b'summary', item[b'description'], {b'type': b'html'})
        for enclosure in item[b'enclosures']:
            handler.addQuickElement(b'link', b'', {b'rel': b'enclosure', 
               b'href': enclosure.url, 
               b'length': enclosure.length, 
               b'type': enclosure.mime_type})

        for cat in item[b'categories']:
            handler.addQuickElement(b'category', b'', {b'term': cat})

        if item[b'item_copyright'] is not None:
            handler.addQuickElement(b'rights', item[b'item_copyright'])
        return

    @property
    def mime_type(self):
        warnings.warn(b'The mime_type attribute of Atom1Feed is deprecated. Use content_type instead.', RemovedInDjango20Warning, stacklevel=2)
        return self.content_type


DefaultFeed = Rss201rev2Feed