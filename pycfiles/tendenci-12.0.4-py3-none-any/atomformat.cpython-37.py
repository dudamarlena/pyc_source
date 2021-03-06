# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/notifications/atomformat.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 22509 bytes
from xml.sax.saxutils import XMLGenerator
from datetime import datetime
from urllib.parse import urlparse
GENERATOR_TEXT = 'django-atompub'
GENERATOR_ATTR = {'uri':'http://code.google.com/p/django-atompub/', 
 'version':'r33'}

class SimplerXMLGenerator(XMLGenerator):

    def addQuickElement(self, name, contents=None, attrs=None):
        """Convenience method for adding an element with no children"""
        if attrs is None:
            attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            self.characters(contents)
        self.endElement(name)


def rfc3339_date(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def get_tag_uri(url, date):
    """Creates a TagURI. See http://diveintomark.org/archives/2004/05/28/howto-atom-id"""
    parts = urlparse(url)
    date_part = ''
    if date is not None:
        date_part = ',%s:' % date.strftime('%Y-%m-%d')
    return 'tag:%s%s%s/%s' % (
     parts.hostname,
     date_part,
     parts.path,
     parts.fragment)


class Feed(object):
    VALIDATE = True

    def __init__(self, slug, feed_url):
        pass

    def __get_dynamic_attr(self, attname, obj, default=None):
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default
        else:
            if callable(attr):
                if hasattr(attr, '__code__'):
                    argcount = attr.__code__.co_argcount
                else:
                    argcount = attr.__call__.__code__.co_argcount
                if argcount == 2:
                    return attr(obj)
                return attr()
            return attr

    def get_feed(self, extra_params=None):
        if extra_params:
            try:
                obj = self.get_object(extra_params.split('/'))
            except (AttributeError, LookupError):
                raise LookupError('Feed does not exist')

        else:
            obj = None
        feed = AtomFeed(atom_id=(self._Feed__get_dynamic_attr('feed_id', obj)),
          title=(self._Feed__get_dynamic_attr('feed_title', obj)),
          updated=(self._Feed__get_dynamic_attr('feed_updated', obj)),
          icon=(self._Feed__get_dynamic_attr('feed_icon', obj)),
          logo=(self._Feed__get_dynamic_attr('feed_logo', obj)),
          rights=(self._Feed__get_dynamic_attr('feed_rights', obj)),
          subtitle=(self._Feed__get_dynamic_attr('feed_subtitle', obj)),
          authors=self._Feed__get_dynamic_attr('feed_authors', obj, default=[]),
          categories=self._Feed__get_dynamic_attr('feed_categories', obj, default=[]),
          contributors=self._Feed__get_dynamic_attr('feed_contributors', obj, default=[]),
          links=self._Feed__get_dynamic_attr('feed_links', obj, default=[]),
          extra_attrs=(self._Feed__get_dynamic_attr('feed_extra_attrs', obj)),
          hide_generator=self._Feed__get_dynamic_attr('hide_generator', obj, default=False))
        items = self._Feed__get_dynamic_attr('items', obj)
        if items is None:
            raise LookupError('Feed has no items field')
        for item in items:
            feed.add_item(atom_id=(self._Feed__get_dynamic_attr('item_id', item)),
              title=(self._Feed__get_dynamic_attr('item_title', item)),
              updated=(self._Feed__get_dynamic_attr('item_updated', item)),
              content=(self._Feed__get_dynamic_attr('item_content', item)),
              published=(self._Feed__get_dynamic_attr('item_published', item)),
              rights=(self._Feed__get_dynamic_attr('item_rights', item)),
              source=(self._Feed__get_dynamic_attr('item_source', item)),
              summary=(self._Feed__get_dynamic_attr('item_summary', item)),
              authors=self._Feed__get_dynamic_attr('item_authors', item, default=[]),
              categories=self._Feed__get_dynamic_attr('item_categories', item, default=[]),
              contributors=self._Feed__get_dynamic_attr('item_contributors', item, default=[]),
              links=self._Feed__get_dynamic_attr('item_links', item, default=[]),
              extra_attrs=self._Feed__get_dynamic_attr('item_extra_attrs', None, default={}))

        if self.VALIDATE:
            feed.validate()
        return feed


class ValidationError(Exception):
    pass


class AtomFeed(object):
    mime_type = 'application/atom+xml'
    ns = 'http://www.w3.org/2005/Atom'

    def __init__(self, atom_id, title, updated=None, icon=None, logo=None, rights=None, subtitle=None, authors=[], categories=[], contributors=[], links=[], extra_attrs={}, hide_generator=False):
        if atom_id is None:
            raise LookupError('Feed has no feed_id field')
        if title is None:
            raise LookupError('Feed has no feed_title field')
        self.feed = {'id':atom_id, 
         'title':title, 
         'updated':updated, 
         'icon':icon, 
         'logo':logo, 
         'rights':rights, 
         'subtitle':subtitle, 
         'authors':authors, 
         'categories':categories, 
         'contributors':contributors, 
         'links':links, 
         'extra_attrs':extra_attrs, 
         'hide_generator':hide_generator}
        self.items = []

    def add_item(self, atom_id, title, updated, content=None, published=None, rights=None, source=None, summary=None, authors=[], categories=[], contributors=[], links=[], extra_attrs={}):
        if atom_id is None:
            raise LookupError('Feed has no item_id method')
        if title is None:
            raise LookupError('Feed has no item_title method')
        if updated is None:
            raise LookupError('Feed has no item_updated method')
        self.items.append({'id':atom_id, 
         'title':title, 
         'updated':updated, 
         'content':content, 
         'published':published, 
         'rights':rights, 
         'source':source, 
         'summary':summary, 
         'authors':authors, 
         'categories':categories, 
         'contributors':contributors, 
         'links':links, 
         'extra_attrs':extra_attrs})

    def latest_updated(self):
        """
        Returns the latest item's updated or the current time if there are no items.
        """
        updates = [item['updated'] for item in self.items]
        if len(updates) > 0:
            updates.sort()
            return updates[(-1)]
        return datetime.now()

    def write_text_construct(self, handler, element_name, data):
        if isinstance(data, tuple):
            text_type, text = data
            if text_type == 'xhtml':
                handler.startElement(element_name, {'type': text_type})
                handler._write(text)
                handler.endElement(element_name)
            else:
                handler.addQuickElement(element_name, text, {'type': text_type})
        else:
            handler.addQuickElement(element_name, data)

    def write_person_construct(self, handler, element_name, person):
        handler.startElement(element_name, {})
        handler.addQuickElement('name', person['name'])
        if 'uri' in person:
            handler.addQuickElement('uri', person['uri'])
        if 'email' in person:
            handler.addQuickElement('email', person['email'])
        handler.endElement(element_name)

    def write_link_construct(self, handler, link):
        if 'length' in link:
            link['length'] = str(link['length'])
        handler.addQuickElement('link', None, link)

    def write_category_construct(self, handler, category):
        handler.addQuickElement('category', None, category)

    def write_source(self, handler, data):
        handler.startElement('source', {})
        if data.get('id'):
            handler.addQuickElement('id', data['id'])
        if data.get('title'):
            self.write_text_construct(handler, 'title', data['title'])
        if data.get('subtitle'):
            self.write_text_construct(handler, 'subtitle', data['subtitle'])
        if data.get('icon'):
            handler.addQuickElement('icon', data['icon'])
        if data.get('logo'):
            handler.addQuickElement('logo', data['logo'])
        if data.get('updated'):
            handler.addQuickElement('updated', rfc3339_date(data['updated']))
        for category in data.get('categories', []):
            self.write_category_construct(handler, category)

        for link in data.get('links', []):
            self.write_link_construct(handler, link)

        for author in data.get('authors', []):
            self.write_person_construct(handler, 'author', author)

        for contributor in data.get('contributors', []):
            self.write_person_construct(handler, 'contributor', contributor)

        if data.get('rights'):
            self.write_text_construct(handler, 'rights', data['rights'])
        handler.endElement('source')

    def write_content(self, handler, data):
        if isinstance(data, tuple):
            content_dict, text = data
            if content_dict.get('type') == 'xhtml':
                handler.startElement('content', content_dict)
                handler._write(text)
                handler.endElement('content')
            else:
                handler.addQuickElement('content', text, content_dict)
        else:
            handler.addQuickElement('content', data)

    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        feed_attrs = {'xmlns': self.ns}
        if self.feed.get('extra_attrs'):
            feed_attrs.update(self.feed['extra_attrs'])
        else:
            handler.startElement('feed', feed_attrs)
            handler.addQuickElement('id', self.feed['id'])
            self.write_text_construct(handler, 'title', self.feed['title'])
            if self.feed.get('subtitle'):
                self.write_text_construct(handler, 'subtitle', self.feed['subtitle'])
            if self.feed.get('icon'):
                handler.addQuickElement('icon', self.feed['icon'])
            if self.feed.get('logo'):
                handler.addQuickElement('logo', self.feed['logo'])
            if self.feed['updated']:
                handler.addQuickElement('updated', rfc3339_date(self.feed['updated']))
            else:
                handler.addQuickElement('updated', rfc3339_date(self.latest_updated()))
        for category in self.feed['categories']:
            self.write_category_construct(handler, category)

        for link in self.feed['links']:
            self.write_link_construct(handler, link)

        for author in self.feed['authors']:
            self.write_person_construct(handler, 'author', author)

        for contributor in self.feed['contributors']:
            self.write_person_construct(handler, 'contributor', contributor)

        if self.feed.get('rights'):
            self.write_text_construct(handler, 'rights', self.feed['rights'])
        if not self.feed.get('hide_generator'):
            handler.addQuickElement('generator', GENERATOR_TEXT, GENERATOR_ATTR)
        self.write_items(handler)
        handler.endElement('feed')

    def write_items(self, handler):
        for item in self.items:
            entry_attrs = item.get('extra_attrs', {})
            handler.startElement('entry', entry_attrs)
            handler.addQuickElement('id', item['id'])
            self.write_text_construct(handler, 'title', item['title'])
            handler.addQuickElement('updated', rfc3339_date(item['updated']))
            if item.get('published'):
                handler.addQuickElement('published', rfc3339_date(item['published']))
            if item.get('rights'):
                self.write_text_construct(handler, 'rights', item['rights'])
            if item.get('source'):
                self.write_source(handler, item['source'])
            for author in item['authors']:
                self.write_person_construct(handler, 'author', author)

            for contributor in item['contributors']:
                self.write_person_construct(handler, 'contributor', contributor)

            for category in item['categories']:
                self.write_category_construct(handler, category)

            for link in item['links']:
                self.write_link_construct(handler, link)

            if item.get('summary'):
                self.write_text_construct(handler, 'summary', item['summary'])
            if item.get('content'):
                self.write_content(handler, item['content'])
            handler.endElement('entry')

    def validate(self):

        def validate_text_construct(obj):
            if isinstance(obj, tuple):
                if obj[0] not in ('text', 'html', 'xhtml'):
                    return False
            return True

        if not validate_text_construct(self.feed['title']):
            raise ValidationError('feed title has invalid type')
        elif self.feed.get('subtitle'):
            if not validate_text_construct(self.feed['subtitle']):
                raise ValidationError('feed subtitle has invalid type')
            elif self.feed.get('rights') and not validate_text_construct(self.feed['rights']):
                raise ValidationError('feed rights has invalid type')
            alternate_links = {}
            for link in self.feed.get('links'):
                if not link.get('rel') == 'alternate':
                    if link.get('rel') is None:
                        key = (
                         link.get('type'), link.get('hreflang'))
                        if key in alternate_links:
                            raise ValidationError('alternate links must have unique type/hreflang')
                    alternate_links[key] = link

            if self.feed.get('authors'):
                feed_author = True
        else:
            feed_author = False
        for item in self.items:
            if (feed_author or item.get('authors') or item.get)('source'):
                if item['source'].get('authors'):
                    pass
                else:
                    raise ValidationError('if no feed author, all entries must have author (possibly in source)')
                if not validate_text_construct(item['title']):
                    raise ValidationError('entry title has invalid type')
                if item.get('rights') and not validate_text_construct(item['rights']):
                    raise ValidationError('entry rights has invalid type')
                if item.get('summary') and not validate_text_construct(item['summary']):
                    raise ValidationError('entry summary has invalid type')
                source = item.get('source')
                if source:
                    if source.get('title') and not validate_text_construct(source['title']):
                        raise ValidationError('source title has invalid type')
                    if source.get('subtitle') and not validate_text_construct(source['subtitle']):
                        raise ValidationError('source subtitle has invalid type')
                    if source.get('rights'):
                        if not validate_text_construct(source['rights']):
                            raise ValidationError('source rights has invalid type')
                alternate_links = {}
                for link in item.get('links'):
                    if not link.get('rel') == 'alternate':
                        if link.get('rel') is None:
                            key = (
                             link.get('type'), link.get('hreflang'))
                            if key in alternate_links:
                                raise ValidationError('alternate links must have unique type/hreflang')
                        alternate_links[key] = link

                if not (item.get('content') or alternate_links):
                    raise ValidationError('if no content, entry must have alternate link')
                if item.get('content'):
                    if isinstance(item.get('content'), tuple):
                        content_type = item.get('content')[0].get('type')
                        if item.get('content')[0].get('src'):
                            if item.get('content')[1]:
                                raise ValidationError('content with src should be empty')
                            if not item.get('summary'):
                                raise ValidationError('content with src requires a summary too')
                            if content_type in ('text', 'html', 'xhtml'):
                                raise ValidationError('content with src cannot have type of text, html or xhtml')
                    if content_type:
                        if '/' in content_type:
                            if not content_type.startswith('text/'):
                                if not (content_type.endswith('/xml') or content_type.endswith('+xml')):
                                    if content_type not in ('application/xml-external-parsed-entity',
                                                            'application/xml-dtd'):
                                        if not item.get('summary'):
                                            raise ValidationError('content in Base64 requires a summary too')
                        if content_type not in ('text', 'html', 'xhtml'):
                            if '/' not in content_type:
                                raise ValidationError('content type does not appear to be valid')
                        return


class LegacySyndicationFeed(AtomFeed):
    __doc__ = '\n    Provides an SyndicationFeed-compatible interface in its __init__ and\n    add_item but is really a new AtomFeed object.\n    '

    def __init__(self, title, link, description, language=None, author_email=None, author_name=None, author_link=None, subtitle=None, categories=[], feed_url=None, feed_copyright=None):
        atom_id = link
        title = title
        updated = None
        rights = feed_copyright
        subtitle = subtitle
        author_dict = {'name': author_name}
        if author_link:
            author_dict['uri'] = author_link
        else:
            if author_email:
                author_dict['email'] = author_email
            authors = [
             author_dict]
            if categories:
                categories = [{'term': term} for term in categories]
            links = [
             {'rel':'alternate', 
              'href':link}]
            if feed_url:
                links.append({'rel':'self',  'href':feed_url})
            if language:
                extra_attrs = {'xml:lang': language}
            else:
                extra_attrs = {}
        AtomFeed.__init__(self, atom_id, title, updated, rights=rights, subtitle=subtitle, authors=authors,
          categories=categories,
          links=links,
          extra_attrs=extra_attrs)

    def add_item(self, title, link, description, author_email=None, author_name=None, author_link=None, pubdate=None, comments=None, unique_id=None, enclosure=None, categories=[], item_copyright=None):
        if unique_id:
            atom_id = unique_id
        else:
            atom_id = get_tag_uri(link, pubdate)
        title = title
        updated = pubdate
        if item_copyright:
            rights = item_copyright
        else:
            rights = None
        if description:
            summary = (
             'html', description)
        else:
            summary = None
        author_dict = {'name': author_name}
        if author_link:
            author_dict['uri'] = author_link
        if author_email:
            author_dict['email'] = author_email
        authors = [
         author_dict]
        categories = [{'term': term} for term in categories]
        links = [{'rel':'alternate',  'href':link}]
        if enclosure:
            links.append({'rel':'enclosure',  'href':enclosure.url,  'length':enclosure.length,  'type':enclosure.mime_type})
        AtomFeed.add_item(self, atom_id, title, updated, rights=rights, summary=summary, authors=authors,
          categories=categories,
          links=links)