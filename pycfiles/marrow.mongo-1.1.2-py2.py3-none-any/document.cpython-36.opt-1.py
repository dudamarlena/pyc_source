# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/document.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 8471 bytes
from __future__ import unicode_literals
from collections import MutableMapping
from bson import ObjectId
from bson.json_util import dumps, loads
from ...package.loader import load
from ...package.canonical import name as named
from ...schema import Attributes, Container
from ...schema.compat import str, unicode, odict
from ..util import SENTINEL
from .field import Field
from .field.alias import Alias
from .index import Index
__all__ = [
 'Document']

class Document(Container):
    __doc__ = 'A MongoDB document definition.\n\t\n\tThis is the top-level class your own document schemas should subclass. They may also subclass eachother; field\n\tdeclaration order is preserved, with subclass fields coming after those provided by the parent class(es). Any\n\tfields redefined will have their original position preserved. Fields may be disabled in subclasses by assigning\n\t`None` to the attribute within the subclass; this is not recommended, though supported to ease testing.\n\t\n\tTraits, Document sub-classes to be used as mix-ins, are provided to augment and specialize behaviour.\n\t'
    __store__ = odict
    __foreign__ = {'object'}
    __type_store__ = None
    __pk__ = None
    __fields__ = Attributes(only=Field)
    __fields__.__sequence__ = 10000
    __indexes__ = Attributes(only=Index)
    __indexes__.__sequence__ = 10000

    def __init__(self, *args, **kw):
        prepare_defaults = kw.pop('_prepare_defaults', True)
        fields = iter((k, v) for k, v in self.__fields__.items() if not k.startswith('__') if isinstance(v, Field) if v.positional)
        for arg in args:
            for name, field in fields:
                if name in kw:
                    raise TypeError('Positional value overridden by keyword argument: ' + name)
                kw[name] = arg
                break

        (super(Document, self).__init__)(**kw)
        if prepare_defaults:
            self._prepare_defaults()

    def _prepare_defaults(self):
        """Trigger assignment of default values."""
        for name, field in self.__fields__.items():
            if field.assign:
                getattr(self, name)

    @classmethod
    def from_mongo(cls, doc):
        """Convert data coming in from the MongoDB wire driver into a Document instance."""
        if doc is None:
            return
        else:
            if isinstance(doc, Document):
                return doc
            if cls.__type_store__:
                if cls.__type_store__ in doc:
                    cls = load(doc[cls.__type_store__], 'marrow.mongo.document')
            instance = cls(_prepare_defaults=False)
            instance.__data__ = doc
            instance._prepare_defaults()
            return instance

    @classmethod
    def from_json(cls, json):
        """Convert JSON data into a Document instance."""
        deserialized = loads(json)
        return cls.from_mongo(deserialized)

    def to_json(self, *args, **kw):
        """Convert our Document instance back into JSON data. Additional arguments are passed through."""
        return dumps(self, *args, **kw)

    @property
    def as_rest(self):
        """Prepare a REST API-safe version of this document.
                
                This, or your overridden version in subclasses, must return a value that `json.dumps` can process, with the
                assistance of PyMongo's `bson.json_util` extended encoding. For details on the latter bit, see:
                
                https://docs.mongodb.com/manual/reference/mongodb-extended-json/
                """
        return self

    def __repr__(self, *args, **kw):
        """A generic programmers' representation of documents.
                
                We add a little non-standard protocol on top of Python's own `__repr__`, allowing passing of additional
                positional or keyword paramaters for inclusion in the result. This allows subclasses to define additional
                information not based on simple field presence.
                """
        parts = []
        if self.__pk__:
            pk = getattr(self, self.__pk__, None)
            if isinstance(pk, ObjectId):
                pk = unicode(pk)
            else:
                if isinstance(pk, (str, unicode)):
                    pass
                else:
                    pk = repr(pk)
            parts.append(pk)
        else:
            parts.extend(args)
            for name, field in self.__fields__.items():
                if name == self.__pk__:
                    pass
                else:
                    if field.repr is not None:
                        if callable(field.repr):
                            if not field.repr(self, field):
                                continue
                        else:
                            if not field.repr:
                                continue
                        value = getattr(self, name, None)
                        if value:
                            parts.append(name + '=' + repr(value))

            for k in kw:
                parts.append(k + '=' + repr(kw[k]))

            if self.__type_store__:
                cls = self.get(self.__type_store__, named(self.__class__))
            else:
                cls = self.__class__.__name__
        return '{0}({1})'.format(cls, ', '.join(parts))

    def __getitem__(self, name):
        """Retrieve data from the backing store."""
        return self.__data__[name]

    def __setitem__(self, name, value):
        """Assign data directly to the backing store."""
        self.__data__[name] = value

    def __delitem__(self, name):
        """Unset a value from the backing store."""
        del self.__data__[name]

    def __iter__(self):
        """Iterate the names of the values assigned to our backing store."""
        return iter(self.__data__.keys())

    def __len__(self):
        """Retrieve the size of the backing store."""
        return len(getattr(self, '__data__', {}))

    def keys(self):
        """Iterate the keys assigned to the backing store."""
        return self.__data__.keys()

    def items(self):
        """Iterate 2-tuple pairs of (key, value) from the backing store."""
        return self.__data__.items()

    iteritems = items

    def values(self):
        """Iterate the values within the backing store."""
        return self.__data__.values()

    def __contains__(self, key):
        """Determine if the given key is present in the backing store."""
        return key in self.__data__

    def __eq__(self, other):
        """Equality comparison between the backing store and other value."""
        return self.__data__ == other

    def __ne__(self, other):
        """Inverse equality comparison between the backing store and other value."""
        return self.__data__ != other

    def get(self, key, default=None):
        """Retrieve a value from the backing store with a default value."""
        return self.__data__.get(key, default)

    def clear(self):
        """Empty the backing store of data."""
        self.__data__.clear()

    def pop(self, name, default=SENTINEL):
        """Retrieve and remove a value from the backing store, optionally with a default."""
        if default is SENTINEL:
            return self.__data__.pop(name)
        else:
            return self.__data__.pop(name, default)

    def popitem(self):
        """Pop an item 2-tuple off the backing store."""
        return self.__data__.popitem()

    def update(self, *args, **kw):
        """Update the backing store directly."""
        (self.__data__.update)(*args, **kw)

    def setdefault(self, key, value=None):
        """Set a value in the backing store if no value is currently present."""
        return self.__data__.setdefault(key, value)


MutableMapping.register(Document)