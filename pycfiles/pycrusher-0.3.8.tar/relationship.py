# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/relationship.py
# Compiled at: 2017-01-13 23:45:16
import six
from .pageitem import PageItem
from .pageitem import NonePageItemSingleton
from .utils import safe_int

class Relationship(object):
    """A Relationhip represents relationship between a Node and interesting
    information regarding the Node.

    This is a summary returned alongside the Node details information, e.g.
    ad call to /organizatin/example will return many properties and many
    relationships.

    To get more details of this relationship, call :class:`CrunchBase`'s
    :meth:`more`.
    """

    def __init__(self, name, data):
        try:
            self.cardinality = data.get('cardinality')
        except Exception:
            self.cardinality = None

        self._name = name
        if self.cardinality in ('OneToMany', 'ManyToMany'):
            self.buildPage(name, data)
        elif self.cardinality in ('OneToOne', ):
            self.buildPageItem(data.get('item'))
        else:
            self.buildPageItem(data)
        return

    def buildPage(self, name, data):
        self.name = name
        paging = data.get('paging')
        self.total_items = safe_int(paging.get('total_items')) or 0
        self.first_page_url = paging.get('first_page_url')
        self.sort_order = paging.get('sort_order')
        self.items = [ PageItem.build(item) for item in data.get('items') ]

    def buildPageItem(self, item):
        if isinstance(item, list):
            self.items = [ PageItem.build(i) for i in item if i ]
            return
        if not item or not hasattr(item, 'get'):
            return NonePageItemSingleton
        node = PageItem.build(item)
        self.items = [node]
        for prop in node.KNOWN_PROPERTIES:
            setattr(self, prop, getattr(node, prop))

        for prop in node.KNOWN_RELATIONSHIPS:
            setattr(self, prop, getattr(node, prop))

    def __getitem__(self, key):
        """Allows caller to use array indices to get a :class:`PageItem`

        Args:
            i (int): 0-based index of the element to retrieve

        Returns:
            PageItem: if valid item exists at index i
            None if the index is too small or too large
        """
        if not isinstance(key, int):
            raise TypeError()
        return self.items[key]

    def __len__(self):
        """Returns the number of items this Page holds"""
        if hasattr(self, 'items'):
            return len(self.items)
        return 0

    def __iter__(self):
        """Allows callers to iterate through the items of this page as such:

            team_members = [member for member in page_of_members]
        """
        return iter(self.items)

    def get(self, i):
        """Gets the i-th element of this page

        Args:
            i (int): 0-based index of the element to retrieve

        Returns:
            PageItem: if valid item exists at index i
            None if the index is too small or too large
        """
        return self[i]

    def __str__(self):
        if self.cardinality is None or self.cardinality == 'OneToOne':
            return str(self.items)
        else:
            return ('{name} Total: {total} {url}').format(name=self._name, total=self.total_items, url=self.first_page_url)
            return

    def __repr__(self):
        return self.__str__()


@six.python_2_unicode_compatible
class NoneRelationship(Relationship):

    def __init__(self):
        super(NoneRelationship, self).__init__(None, {'cardinality': 'OneToMany', 'paging': {}, 'items': {}})
        return

    def get(self, _):
        return NonePageItemSingleton

    def __len__(self):
        return 0

    def __str__(self):
        return 'NoneRelationship'


NoneRelationshipSingleton = NoneRelationship()