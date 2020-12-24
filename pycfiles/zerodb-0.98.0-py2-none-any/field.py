# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/catalog/indexes/field.py
# Compiled at: 2016-04-22 11:29:50
import itertools as it, six
from persistent import Persistent
from ZODB.broken import Broken
from zerodbext.catalog.indexes.field import CatalogFieldIndex as _CatalogFieldIndex
from zerodbext.catalog.indexes.common import CatalogIndex
from zerodbext.catalog import RangeValue
from zerodb import trees
from zerodb.catalog.indexes.common import CallableDiscriminatorMixin
from zerodb.util.iter import ListPrefetch
_marker = ()
threshold = 10

def multiunion1(set_type, seqs):
    result = set_type()
    for s in seqs:
        if isinstance(s, six.integer_types):
            s = (
             s,)
        result.update(s)

    return result


class NewTreeItems(object):

    def __init__(self, items):
        self.items = items
        self.iterator = iter(items)

    def __getitem__(self, i):
        v = self.items.__getitem__(i)
        if isinstance(v, int):
            return (v,)
        else:
            return v

    def __len__(self):
        return self.items.__len__()

    def __iter__(self):
        for nextobj in self.iterator:
            if isinstance(nextobj, int):
                yield (
                 nextobj,)
            else:
                yield nextobj


class CatalogFieldIndex(CallableDiscriminatorMixin, _CatalogFieldIndex):
    family = trees.family32

    def __init__(self, discriminator):
        self._init_discriminator(discriminator)
        self._not_indexed = self.family.IF.Set()
        self.clear()

    def applyInRange(self, start, end, excludemin=False, excludemax=False):
        return ListPrefetch(lambda : it.chain.from_iterable(ListPrefetch(lambda : NewTreeItems(self._fwd_index.values(start, end, excludemin=excludemin, excludemax=excludemax)))))

    def applyEq(self, value):
        Set = self.family.IF.Set
        docs = self._fwd_index.get(value, None)
        if docs is None:
            return Set()
        else:
            if isinstance(docs, six.integer_types):
                return Set([docs])
            else:
                if isinstance(docs, tuple):
                    return Set(docs)
                return ListPrefetch(lambda : iter(docs))

            return

    def scan_forward(self, docids, limit=None):
        fwd_index = ListPrefetch(lambda : self._fwd_index.values())
        n = 0
        for curdocids in fwd_index:
            if isinstance(curdocids, int) and curdocids in docids:
                n += 1
                yield curdocids
                if limit and n >= limit:
                    raise StopIteration
            elif isinstance(curdocids, (tuple, self.family.IF.TreeSet)):
                for docid in curdocids:
                    if docid in docids:
                        n += 1
                        yield docid
                        if limit and n >= limit:
                            raise StopIteration

    def index_doc(self, docid, obj):
        if self.discriminator_callable:
            virtuals = getattr(obj.__class__, '_z_virtual_fields', {})
            value = virtuals.get(self.discriminator, _marker)
            if value != _marker:
                try:
                    value = value(obj)
                except:
                    value = _marker

        else:
            value = getattr(obj, self.discriminator, _marker)
        if value is _marker:
            super(CatalogIndex, self).unindex_doc(docid)
            self._not_indexed.add(docid)
            return None
        else:
            if isinstance(value, Persistent):
                raise ValueError('Catalog cannot index persistent object %s' % value)
            if isinstance(value, Broken):
                raise ValueError('Catalog cannot index broken object %s' % value)
            if docid in self._not_indexed:
                self._not_indexed.remove(docid)
            return self.inner_index_doc(docid, value)

    def inner_index_doc(self, docid, value):
        """See interface IInjection"""
        rev_index = self._rev_index
        if docid in rev_index:
            docids = self._fwd_index.get(value, ())
            if isinstance(docids, int):
                if docids == docid:
                    return
            elif docid in docids:
                return
            self.unindex_doc(docid)
        curdocids = self._fwd_index.get(value)
        if curdocids is None:
            self._fwd_index[value] = docid
        else:
            newdocids = curdocids
            if isinstance(curdocids, int):
                newdocids = (
                 curdocids,)
            elif isinstance(curdocids, tuple) and len(curdocids) >= threshold - 1:
                newdocids = self.family.IF.TreeSet(curdocids)
                self._fwd_index[value] = newdocids
            if isinstance(newdocids, tuple):
                newdocids += (docid,)
                self._fwd_index[value] = newdocids
            elif isinstance(newdocids, self.family.IF.TreeSet):
                newdocids.insert(docid)
        self._num_docs.change(1)
        rev_index[docid] = value
        return

    def search(self, queries, operator='or'):
        sets = []
        for query in queries:
            if isinstance(query, RangeValue):
                query = query.as_tuple()
            else:
                query = (
                 query, query)
            set = multiunion1(self.family.IF.Set, self._fwd_index.values(*query))
            sets.append(set)

        result = None
        if len(sets) == 1:
            result = sets[0]
        elif operator == 'and':
            sets.sort()
            for set in sets:
                result = self.family.IF.intersection(set, result)

        else:
            result = self.family.IF.multiunion(sets)
        return result

    def unindex_doc(self, docid):
        """See interface IInjection.
        Base class overridden to be able to unindex None values.
        """
        _not_indexed = self._not_indexed
        if docid in _not_indexed:
            _not_indexed.remove(docid)
        rev_index = self._rev_index
        value = rev_index.get(docid, _marker)
        if value is _marker:
            return
        del rev_index[docid]
        delvalue = False
        try:
            docids = self._fwd_index[value]
            if isinstance(docids, int):
                delvalue = True
            elif isinstance(docids, tuple):
                newtuple = []
                for i in docids:
                    if i != docid:
                        newtuple.append(i)

                if len(newtuple) == 0:
                    delvalue = True
                else:
                    self._fwd_index[value] = tuple(newtuple)
            elif isinstance(docids, self.family.IF.TreeSet):
                set = self._fwd_index[value]
                set.remove(docid)
                if not set:
                    delvalue = True
        except KeyError:
            pass

        if delvalue:
            del self._fwd_index[value]
        self._num_docs.change(-1)