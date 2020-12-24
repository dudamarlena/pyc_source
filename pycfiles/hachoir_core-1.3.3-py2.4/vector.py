# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/vector.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.field import Field, FieldSet, ParserError

class GenericVector(FieldSet):
    __module__ = __name__

    def __init__(self, parent, name, nb_items, item_class, item_name='item', description=None):
        assert issubclass(item_class, Field)
        assert isinstance(item_class.static_size, (int, long))
        if not 0 < nb_items:
            raise ParserError('Unable to create empty vector "%s" in %s' % (name, parent.path))
        size = nb_items * item_class.static_size
        self.__nb_items = nb_items
        self._item_class = item_class
        self._item_name = item_name
        FieldSet.__init__(self, parent, name, description, size=size)

    def __len__(self):
        return self.__nb_items

    def createFields(self):
        name = self._item_name + '[]'
        parser = self._item_class
        for index in xrange(len(self)):
            yield parser(self, name)


class UserVector(GenericVector):
    """
    To implement:
    - item_name: name of a field without [] (eg. "color" becomes "color[0]"),
      default value is "item"
    - item_class: class of an item
    """
    __module__ = __name__
    item_class = None
    item_name = 'item'

    def __init__(self, parent, name, nb_items, description=None):
        GenericVector.__init__(self, parent, name, nb_items, self.item_class, self.item_name, description)