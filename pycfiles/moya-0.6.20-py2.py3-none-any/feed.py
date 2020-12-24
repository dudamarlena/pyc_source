# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/feed.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from __future__ import print_function
from ..elements.elementbase import LogicElement, Attribute
from ..tags.context import DataSetter
from ..interface import AttributeExposer
from ..compat import iteritems, text_type

class Feed(AttributeExposer):
    __moya_exposed_attributes__ = [
     b'format', b'title', b'_items', b'channel', b'xml']

    def __init__(self, format, url, title, description, link, **kwargs):
        self.format = format
        self.url = url
        self.channel = kwargs
        self.channel.update(title=title, description=description, link=link)
        self._items = []
        super(Feed, self).__init__()

    def __repr__(self):
        return (b"<feed-{} '{}'>").format(self.format, self.title)

    @property
    def title(self):
        return self.channel.get(b'title', None)

    def add_item(self, item):
        self._items.append(item)

    @property
    def xml(self):
        return self.to_xml()

    def to_xml(self):
        from lxml import etree as ET
        feed = ET.Element(b'rss', version=b'2.0', nsmap={b'atom': b'http://www.w3.org/2005/Atom'})
        channel = ET.SubElement(feed, b'channel')
        ET.SubElement(channel, b'{http://www.w3.org/2005/Atom}link', href=self.url, type=b'application/rss+xml', rel=b'self')
        for k, v in iteritems(self.channel):
            if v:
                node = ET.SubElement(channel, k)
                node.text = text_type(v)

        for item in self._items:
            item_node = ET.SubElement(channel, b'item')
            for k, v in iteritems(item):
                if v is not None:
                    node = ET.SubElement(item_node, k)
                    node.text = v

        xml = ET.tostring(feed, encoding=b'utf-8')
        return xml

    def __xml__(self):
        return self.to_xml()


class FeedElement(DataSetter):
    """
    Create a [url http://en.wikipedia.org/wiki/RSS]RSS[/url] Feed object.

    You can add items to a feed with [tag]add-feed-item[/tag].

    """

    class Help:
        synopsis = b'create an RSS feed'
        example = b'\n        <view libname="view.feed">\n            <!-- create feed object -->\n            <get-fq-url name="list" dst="blog_url" />\n            <feed title="${.app.settings.title or \'blog\'}"\n                description="${.app.settings.description or \'blog feed\'}"\n                link="${blog_url}" dst="feed"/>\n\n            <db:query model="#Post" dst="posts" orderby="-published_date"\n                filter="#Post.published==True" maxresults="25"/>\n\n            <!-- add items -->\n            <for src="posts" dst="post">\n                <get-fq-url name="showpost" let:slug="post.slug" dst="post_url"/>\n                <process-markup src="post.content" type="${.app.settings.default_markup}" dst="description"/>\n                <add-feed-item src="feed"\n                    title="post.title" link="post_url" description="description"\n                    pub_date="post.published_date"/>\n            </for>\n\n            <!-- serve feed XML -->\n            <serve-xml content_type="application/rss+xml" obj="feed"/>\n        </view>\n        '

    class Meta:
        tag_name = b'feed'

    dst = Attribute(b'Destination object', type=b'reference', default=None)
    title = Attribute(b'Title of Feed', required=True)
    description = Attribute(b'Description of feed', required=True)
    link = Attribute(b'Link', required=True, default=None)
    language = Attribute(b'Language', required=False, default=None)

    def logic(self, context):
        params = self.get_parameters(context)
        optional = {}
        if params.language is None:
            lang = context[b'.locale.language']
            if lang:
                optional[b'language'] = text_type(lang)
        optional = self.get_let_map(context)
        if b'generator' not in optional:
            optional[b'generator'] = text_type(context[b'.app.lib.version_name'])
        feed = Feed(format=b'rss', url=context[b'.request.url'], title=params.title, description=params.description, link=params.link, **optional)
        self.set_context(context, params.dst, feed)
        return


class AddFeedItem(LogicElement):
    """
    Add an item to a [tag]feed[/tag].
    """

    class Help:
        synopsis = b'add an item to an RSS feed'

    class Meta:
        one_of = [
         ('title', 'description')]

    src = Attribute(b'feed to add to', type=b'expression', required=True)
    title = Attribute(b'Title of Feed', type=b'expression', required=False)
    link = Attribute(b'Link to this item on the web', type=b'expression', required=True, default=None)
    description = Attribute(b'Item description', type=b'expression', required=False)
    author = Attribute(b'Email address of the author of this item', type=b'expression', required=False, default=None)
    category = Attribute(b'Includes the item in one or more categories', type=b'expression', required=False, default=None)
    guid = Attribute(b'A string that uniquely identifies the item.', type=b'expression', required=False, default=None)
    pub_date = Attribute(b'Indicates when the item was published', type=b'expression', required=False, default=None)
    _item_names = [
     ('title', None),
     ('link', None),
     ('description', None),
     ('author', None),
     ('category', None),
     ('guid', None),
     ('pub_date', 'pubDate')]

    def logic(self, context):
        params = self.get_parameters(context)
        item = {}
        for name, item_name in self._item_names:
            if self.has_parameter(name):
                if item_name is None:
                    item_name = name
                item[item_name] = params[name]

        if b'pubDate' in item:
            dt = item[b'pubDate']
            if hasattr(dt, b'rfc2822'):
                item[b'pubDate'] = dt.rfc2822
        if b'guid' not in item:
            guid = item.get(b'link', None)
            item[b'guid'] = guid
        feed = params.src
        try:
            feed.add_item(item)
        except Exception as e:
            self.throw(b'add-feed-item.add-fail', (b'unable to add feed item ({})').format(e))

        return