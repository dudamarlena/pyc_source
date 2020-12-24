# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twitter_client/__init__.py
# Compiled at: 2008-10-28 00:18:06
"""Contains extensions to Atom objects used with Twitter API."""
__author__ = 'livibetter (Yu-Jie Lin)'
import datetime, re, atom
OPENSEARCH_NAMESPACE = 'http://a9.com/-/spec/opensearch/1.1/'
OPENSEARCH_TEMPLATE = '{http://a9.com/-/spec/opensearch/1.1/}%s'
TWITTER_NAMESPACE = 'http://api.twitter.com/'
TWITTER_TEMPLATE = '{http://api.twitter.com/}%s'

class Base(atom.AtomBase):

    def Get(self):
        """Gets self.text in more proper type"""
        return self.text

    def Set(self, text):
        """Sets self.text via more proper type"""
        self.text = text
        return self


class ItemsPerPage(Base):
    _tag = 'itemsPerPage'
    _namespace = OPENSEARCH_NAMESPACE

    def Get(self):
        return int(self.text)

    def Set(self, items):
        """Sets Items Per Page

    Args:
      items: int The number of items per page
    """
        self.text = str(int(items))
        return self


def ItemsPerPageFromString(xml_string):
    return atom.CreateClassFromXMLString(ItemsPerPage, xml_string)


class Language(Base):
    _tag = 'language'
    _namespace = OPENSEARCH_NAMESPACE


def LanguageFromString(xml_string):
    return atom.CreateClassFromXMLString(Language, xml_string)


class Warning(Base):
    _tag = 'warning'
    _namespace = TWITTER_NAMESPACE


def WarningFromString(xml_string):
    return atom.CreateClassFromXMLString(Warning, xml_string)


class Date(atom.Date):
    _tag = 'date'
    _namespace = atom.ATOM_NAMESPACE

    def Get(self):
        return datetime.datetime.strptime(self.text, '%Y-%m-%dT%H:%M:%SZ')

    def Set(self, date):
        self.text = date.strftime('%Y-%m-%dT%H:%M:%SZ')


def DateFromString(xml_string):
    return atom.CreateClassFromXMLString(Date, xml_string)


class Updated(Date):
    _tag = 'updated'
    _namespace = atom.ATOM_NAMESPACE


def UpdatedFromString(xml_string):
    return atom.CreateClassFromXMLString(Updated, xml_string)


class Published(Date):
    _tag = 'published'
    _namespace = atom.ATOM_NAMESPACE


def PublishedFromString(xml_string):
    return atom.CreateClassFromXMLString(Published, xml_string)


class LinkFinder(atom.LinkFinder):

    def GetLinkByRel(self, rel):
        for link in self.link:
            if rel == link.rel:
                return link

        return


class SearchResultEntry(atom.Entry, LinkFinder):
    """A Twitter Search Result Entry flavor of Atom Entry"""
    _children = atom.Entry._children.copy()
    _children['{%s}published' % atom.ATOM_NAMESPACE] = ('published', Published)
    _children['{%s}updated' % atom.ATOM_NAMESPACE] = ('updated', Updated)

    def __GetId(self):
        return self.__id

    def __SetId(self, id):
        self.__id = id
        if id is not None and id.text is not None:
            self.__id.text = id.text.strip()
        return

    id = property(__GetId, __SetId)
    message_id_pattern = re.compile('tag:search.twitter.com,2005:(\\d+)')

    def GetMessageID(self):
        """Extracts message id from id element"""
        if self.id.text:
            return self.message_id_pattern.match(self.id.text).group(1)
        return


def SearchResultEntryFromString(xml_string):
    return atom.CreateClassFromXMLString(SearchResultEntry, xml_string)


class SearchResultFeed(atom.Feed, LinkFinder):
    """A Twitter Search Result Feed flavor of Atom Feed"""
    _tag = atom.Feed._tag
    _namespace = atom.Feed._namespace
    _children = atom.Feed._children.copy()
    _attributes = atom.Feed._attributes.copy()
    _children['{%s}updated' % atom.ATOM_NAMESPACE] = ('updated', Updated)
    _children['{%s}warning' % TWITTER_NAMESPACE] = (
     'warning', Warning)
    _children['{%s}itemsPerPage' % OPENSEARCH_NAMESPACE] = (
     'items_per_page', ItemsPerPage)
    _children['{%s}language' % OPENSEARCH_NAMESPACE] = (
     'language', Language)
    _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', [SearchResultEntry])
    del _children['{%s}category' % atom.ATOM_NAMESPACE]
    del _children['{%s}generator' % atom.ATOM_NAMESPACE]
    del _children['{%s}author' % atom.ATOM_NAMESPACE]
    del _children['{%s}contributor' % atom.ATOM_NAMESPACE]
    del _children['{%s}logo' % atom.ATOM_NAMESPACE]
    del _children['{%s}icon' % atom.ATOM_NAMESPACE]
    del _children['{%s}rights' % atom.ATOM_NAMESPACE]
    del _children['{%s}subtitle' % atom.ATOM_NAMESPACE]

    def __GetId(self):
        return self.__id

    def __SetId(self, id):
        self.__id = id
        if id is not None and id.text is not None:
            self.__id.text = id.text.strip()
        return

    id = property(__GetId, __SetId)

    def __init__(self, atom_id=None, title=None, entry=None, link=None, warning=None, updated=None, items_per_page=None, language=None, extension_elements=None, extension_attributes=None, text=None):
        """Constructor for Source
    
    Args:
      id: Id (optional) The entry's Id element
      link: list (optional) A list of Link instances
      title: Title (optional) The entry's Title element
      updated: Updated (optional) The entry's Updated element
      entry: list (optional) A list of the Entry instances contained in the 
          feed.
      warning: Warning (optional) The entry's Warning element.
      items_per_page: ItemsPerPage (optional) The entry's ItemsPerPage element of
                      OpenSearch.
      language: Language (optional) The entry's Language element of OpenSearch.
      text: String (optional) The text contents of the element. This is the 
          contents of the Entry's XML text node. 
          (Example: <foo>This is the text</foo>)
      extension_elements: list (optional) A list of ExtensionElement instances
          which are children of this element.
      extension_attributes: dict (optional) A dictionary of strings which are 
          the values for additional XML attributes of this element.
    """
        self.id = atom_id
        self.link = link or []
        self.title = title
        self.updated = updated
        self.entry = entry or []
        self.warning = warning
        self.items_per_page = items_per_page
        self.language = language
        self.text = text
        self.extension_elements = extension_elements or []
        self.extension_attributes = extension_attributes or {}


def SearchResultFeedFromString(xml_string):
    return atom.CreateClassFromXMLString(SearchResultFeed, xml_string)