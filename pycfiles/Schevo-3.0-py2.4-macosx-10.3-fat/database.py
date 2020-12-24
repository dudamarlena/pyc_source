# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/database.py
# Compiled at: 2007-03-21 14:34:41
"""Schevo database.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
import random, louie
from schevo import base
from schevo import change
from schevo.change import CREATE, UPDATE, DELETE
from schevo.constant import UNASSIGNED
from schevo import error
from schevo.entity import Entity
from schevo.extent import Extent
from schevo.field import Entity as EntityField
from schevo.field import not_fget
from schevo import icon
from schevo.lib import module
from schevo.namespace import NamespaceExtension
import schevo.schema
from schevo.signal import TransactionExecuted
from schevo.store.btree import BTree
from schevo.store.connection import Connection
from schevo.store.file_storage import FileStorage
from schevo.store.persistent_dict import PersistentDict as PDict
from schevo.store.persistent_list import PersistentList as PList
from schevo.trace import log
from schevo.transaction import CallableWrapper, Combination, Initialize, Populate, Transaction

def evolve(db, schema_source, version):
    db._evolve(schema_source, version)
    db._on_open()


def inject(filename, schema_source, version):
    fs = FileStorage(filename)
    conn = Connection(fs)
    root = conn.get_root()
    schevo = root['SCHEVO']
    schevo['schema_source'] = schema_source
    schevo['version'] = version
    conn.commit()
    fs.close()


def open(filename=None, schema_source=None, initialize=True, label='', fp=None, cache_size=100000):
    """Return an open database."""
    if fp is not None:
        fs = FileStorage(fp=fp)
    else:
        fs = FileStorage(filename)
    conn = Connection(fs, cache_size)
    db = Database(conn)
    if label:
        db.label = label
    db._sync(schema_source, initialize)
    icon.install(db)
    db._on_open()
    return db


class dummy_lock(object):
    """Dummy class for read_lock and write_lock objects in a database,
    so that code can be written to be multi-thread-ready but still be
    run in cases where the schevo.mt plugin is not installed."""
    __module__ = __name__

    def release(self):
        pass


class schema_counter(object):
    """Schema counter singleton.

    This is a class instead of a global, because globals won't work
    because of the binding done by optimize.bind_all.
    """
    __module__ = __name__
    _current = 0

    @classmethod
    def next(cls):
        c = cls._current
        cls._current += 1
        return c

    @classmethod
    def next_schema_name(cls):
        return 'schevo-db-schema-%i' % cls.next()


class Database(base.Database):
    """Schevo database, using Durus as an object store.

    See doc/reference/database.txt for detailed information on data
    structures, or visit http://docs.schevo.org/trunk/reference/database.html
    """
    __module__ = __name__
    label = 'Schevo Database'
    dispatch = False
    read_lock = dummy_lock
    write_lock = dummy_lock

    def __init__(self, connection):
        """Create a database.

        - `connection`: The Durus connection to use.
        """
        self.connection = connection
        self._root = connection.get_root()
        self._commit = connection.commit
        self._rollback = connection.abort
        self._remembered = []
        self._create_schevo_structures()
        self._commit()
        self._extents = {}
        self._entity_classes = {}
        self._bulk_mode = False
        self._executing = []
        schevo = self._root['SCHEVO']
        self._extent_name_id = schevo['extent_name_id']
        self._extent_maps_by_id = schevo['extents']
        self._update_extent_maps_by_name()
        self._plugins = []

    def __repr__(self):
        return '<Database %r :: V %r>' % (self.label, self.version)

    @property
    def _extent_id_name(self):
        return dict(((v, k) for (k, v) in self._extent_name_id.items()))

    def close(self):
        """Close the database."""
        assert log(1, 'Stopping plugins.')
        p = self._plugins
        while p:
            assert log(2, 'Stopping', p)
            p.pop().close()

        assert log(1, 'Closing storage.')
        self.connection.storage.close()
        del self.connection
        remembered = self._remembered
        while remembered:
            module.forget(remembered.pop())

    def execute(self, *transactions, **kw):
        """Execute transaction(s)."""
        strict = kw.get('strict', True)
        executing = self._executing
        if len(transactions) == 0:
            raise RuntimeError('Must supply at least one transaction.')
        if len(transactions) > 1:
            if not executing:
                raise RuntimeError('Must supply only one top-level transaction.')
            else:
                tx = Combination(transactions)
        else:
            tx = transactions[0]
        if tx._executed:
            raise error.TransactionAlreadyExecuted('%r already executed.' % tx)
        if not executing:
            self._bulk_mode = kw.get('bulk_mode', False)
            strict = True
        bulk_mode = self._bulk_mode
        executing.append(tx)
        assert log(1, 'Begin executing [%i]' % len(executing), tx)
        try:
            retval = tx._execute(self)
            assert log(2, 'Result was', repr(retval))
            for (extent_name, index_spec) in tx._relaxed:
                assert log(2, 'Enforcing index', extent_name, index_spec)
                self._enforce_index(extent_name, index_spec)

            if strict:
                c = tx._changes_requiring_validation
                assert log(2, 'Validating', len(c), 'changes requiring validation')
                self._validate_changes(c)
        except Exception, e:
            assert log(1, e, 'was raised; undoing side-effects.')
            if bulk_mode:
                assert log(2, 'Bulk Mode transaction; storage rollback.')
                self._rollback()
            if len(executing) == 1:
                assert log(2, 'Outer transaction; storage rollback.')
                self._rollback()
            assert log(2, 'Inner transaction; inverting.')
            inversions = tx._inversions
            while len(inversions):
                (method, args, kw) = inversions.pop()
                self._executing = None
                method(*args, **kw)
                self._executing = executing

            executing.pop()
            raise

        assert log(1, ' Done executing [%i]' % len(executing), tx)
        tx._executed = True
        if bulk_mode:
            if len(executing) > 1:
                assert log(2, 'Bulk Mode inner transaction.')
                e2 = executing[(-2)]
                e1 = executing[(-1)]
                strict or e2._changes_requiring_validation.extend(e1._changes_requiring_validation)
        elif bulk_mode:
            assert log(2, 'Bulk Mode outer transaction; storage commit.')
            self._commit()
        elif len(executing) > 1:
            assert log(2, 'Inner transaction; record inversions and changes.')
            e2 = executing[(-2)]
            e1 = executing[(-1)]
            e2._inversions.extend(e1._inversions)
            e2._changes_requiring_notification.extend(e1._changes_requiring_notification)
            if not strict:
                e2._changes_requiring_validation.extend(e1._changes_requiring_validation)
        else:
            assert log(2, 'Outer transaction; storage commit.')
            self._commit()
            if self.dispatch:
                assert log(2, 'Dispatching TransactionExecuted signal.')
                louie.send(TransactionExecuted, sender=self, transaction=tx)
        executing.pop()
        return retval

    def extent(self, extent_name):
        """Return the named extent instance."""
        return self._extents[extent_name]

    def extent_names(self):
        """Return a sorted list of extent names."""
        return sorted(self._extent_maps_by_name.keys())

    def extents(self):
        """Return a list of extent instances sorted by name."""
        extent = self.extent
        return [ extent(name) for name in self.extent_names() ]

    def pack(self):
        """Pack the database."""
        self.connection.pack()

    def populate(self, sample_name=''):
        """Populate the database with sample data."""
        tx = Populate(sample_name)
        self.execute(tx)

    @property
    def format(self):
        return self._root['SCHEVO']['format']

    @property
    def schema_source(self):
        return self._root['SCHEVO']['schema_source']

    @property
    def version(self):
        return self._root['SCHEVO']['version']

    def _append_change(self, typ, extent_name, oid):
        executing = self._executing
        if executing:
            info = (
             typ, extent_name, oid)
            tx = executing[(-1)]
            tx._changes_requiring_validation.append(info)
            if not self._bulk_mode:
                tx._changes_requiring_notification.append(info)

    def _append_inversion(self, method, *args, **kw):
        """Append an inversion to a transaction if one is being
        executed."""
        if self._bulk_mode:
            return
        executing = self._executing
        if executing:
            executing[(-1)]._inversions.append((method, args, kw))

    def _by_entity_oids(self, extent_name, *index_spec):
        """Return a list of OIDs from an extent sorted by index_spec."""
        extent_map = self._extent_map(extent_name)
        indices = extent_map['indices']
        index_map = extent_map['index_map']
        field_names = []
        ascending = []
        for field_name in index_spec:
            if field_name.startswith('-'):
                field_names.append(field_name[1:])
                ascending.append(False)
            else:
                field_names.append(field_name)
                ascending.append(True)

        index_spec = _field_ids(extent_map, field_names)
        if index_spec not in indices:
            if index_spec not in index_map:
                raise error.IndexDoesNotExist('Index %r not found in extent %r.' % (_field_names(extent_map, index_spec), extent_name))
            index_spec = index_map[index_spec][0]
        oids = []
        (unique, branch) = indices[index_spec]
        _walk_index(branch, ascending, oids)
        return oids

    def _create_entity(self, extent_name, fields, oid=None, rev=None):
        """Create a new entity in an extent; return the oid."""
        extent_map = self._extent_map(extent_name)
        entities = extent_map['entities']
        old_next_oid = extent_map['next_oid']
        field_name_id = extent_map['field_name_id']
        entity_field_ids = extent_map['entity_field_ids']
        extent_name_id = self._extent_name_id
        extent_maps_by_id = self._extent_maps_by_id
        indices_added = []
        ia_append = indices_added.append
        links_created = []
        lc_append = links_created.append
        try:
            if oid is None:
                oid = extent_map['next_oid']
                extent_map['next_oid'] += 1
            if rev is None:
                rev = 0
            if oid in entities:
                raise error.EntityExists('OID %r already exists in %r' % (oid, extent_name))
            fields_by_id = PDict()
            new_links = []
            nl_append = new_links.append
            for (name, value) in fields.iteritems():
                field_id = field_name_id[name]
                if field_id in entity_field_ids and isinstance(value, Entity):
                    other_extent_id = extent_name_id[value._extent.name]
                    other_oid = value._oid
                    value = (other_extent_id, other_oid)
                    nl_append((field_id, other_extent_id, other_oid))
                fields_by_id[field_id] = value

            setdefault = fields_by_id.setdefault
            for field_id in field_name_id.itervalues():
                setdefault(field_id, UNASSIGNED)

            indices = extent_map['indices']
            for index_spec in indices.iterkeys():
                field_values = tuple((fields_by_id[field_id] for field_id in index_spec))
                relaxed_specs = self._relaxed[extent_name]
                if index_spec in relaxed_specs:
                    (txns, relaxed) = relaxed_specs[index_spec]
                else:
                    relaxed = None
                _index_add(extent_map, index_spec, relaxed, oid, field_values)
                ia_append((extent_map, index_spec, oid, field_values))

            referrer_extent_id = extent_name_id[extent_name]
            for (referrer_field_id, other_extent_id, other_oid) in new_links:
                other_extent_map = extent_maps_by_id[other_extent_id]
                try:
                    other_entity_map = other_extent_map['entities'][other_oid]
                except KeyError:
                    field_id_name = extent_map['field_id_name']
                    field_name = field_id_name[referrer_field_id]
                    raise error.EntityDoesNotExist('Entity referenced in %r does not exist.' % field_name)

                links = other_entity_map['links']
                link_key = (referrer_extent_id, referrer_field_id)
                if link_key not in links:
                    links[link_key] = BTree()
                links[link_key][oid] = None
                other_entity_map['link_count'] += 1
                lc_append((other_entity_map, links, link_key, oid))

            entity_map = entities[oid] = PDict()
            entity_map['rev'] = rev
            entity_map['fields'] = fields_by_id
            entity_map['link_count'] = 0
            entity_map['links'] = PDict()
            extent_map['len'] += 1
            self._append_inversion(self._delete_entity, extent_name, oid)
            append_change = self._append_change
            append_change(CREATE, extent_name, oid)
            return oid
        except:
            for (_e, _i, _o, _f) in indices_added:
                _index_remove(_e, _i, _o, _f)

            for (other_entity_map, links, link_key, oid) in links_created:
                del links[link_key][oid]
                other_entity_map['link_count'] -= 1

            extent_map['next_oid'] = old_next_oid
            raise

        return

    def _delete_entity(self, extent_name, oid):
        (entity_map, extent_map) = self._entity_extent_map(extent_name, oid)
        extent_id = extent_map['id']
        extent_name_id = self._extent_name_id
        extent_maps_by_id = self._extent_maps_by_id
        entity_field_ids = extent_map['entity_field_ids']
        field_name_id = extent_map['field_name_id']
        link_count = entity_map['link_count']
        links = entity_map['links']
        deletes = set()
        executing = self._executing
        if executing:
            tx = executing[(-1)]
            deletes.update([ (extent_name_id[del_entity_cls.__name__], del_oid) for (del_entity_cls, del_oid) in tx._deletes ])
            deletes.update([ (extent_name_id[del_entity_cls.__name__], del_oid) for (del_entity_cls, del_oid) in tx._known_deletes ])
        for ((other_extent_id, other_field_id), others) in links.items():
            for other_oid in others:
                if (
                 other_extent_id, other_oid) in deletes:
                    continue
                if (
                 other_extent_id, other_oid) != (extent_id, oid):
                    msg = 'Cannot delete; other entities depend on this one.'
                    raise error.DeleteRestricted(msg)

        old_fields = self._entity_fields(extent_name, oid)
        old_rev = entity_map['rev']
        indices = extent_map['indices']
        fields_by_id = entity_map['fields']
        for index_spec in indices.iterkeys():
            field_values = tuple((fields_by_id.get(f_id, UNASSIGNED) for f_id in index_spec))
            _index_remove(extent_map, index_spec, oid, field_values)

        referrer_extent_id = extent_name_id[extent_name]
        for referrer_field_id in entity_field_ids:
            other_value = fields_by_id.get(referrer_field_id, UNASSIGNED)
            if isinstance(other_value, tuple):
                (other_extent_id, other_oid) = other_value
                link_key = (referrer_extent_id, referrer_field_id)
                other_extent_map = extent_maps_by_id[other_extent_id]
                if other_oid in other_extent_map['entities']:
                    other_entity_map = other_extent_map['entities'][other_oid]
                    links = other_entity_map['links']
                    other_links = links[link_key]
                    del other_links[oid]
                    other_entity_map['link_count'] -= 1

        del extent_map['entities'][oid]
        extent_map['len'] -= 1
        self._append_inversion(self._create_entity, extent_name, old_fields, oid, old_rev)
        append_change = self._append_change
        append_change(DELETE, extent_name, oid)

    def _enforce_index(self, extent_name, *index_spec):
        """Validate and begin enforcing constraints on the specified
        index if it was relaxed within the currently-executing
        transaction."""
        executing = self._executing
        if not executing:
            return
        extent_map = self._extent_map(extent_name)
        index_spec = _field_ids(extent_map, index_spec)
        indices = extent_map['indices']
        if index_spec not in indices:
            raise error.IndexDoesNotExist('Index %r not found in extent %r.' % (_field_names(extent_map, index_spec), extent_name))
        current_txn = executing[(-1)]
        relaxed = self._relaxed[extent_name]
        (txns, added) = relaxed.get(index_spec, ([], []))
        if not txns:
            return
        if current_txn in txns:
            current_txn._relaxed.remove((extent_name, index_spec))
            txns.remove(current_txn)
        if not txns:
            for (_extent_map, _index_spec, _oid, _field_values) in added:
                _index_validate(_extent_map, _index_spec, _oid, _field_values)

    def _entity(self, extent_name, oid):
        """Return the entity instance."""
        EntityClass = self._entity_classes[extent_name]
        return EntityClass(oid)

    def _entity_field(self, extent_name, oid, name):
        """Return the value of a field in an entity in named extent
        with given OID."""
        (entity_map, extent_map) = self._entity_extent_map(extent_name, oid)
        field_name_id = extent_map['field_name_id']
        entity_field_ids = extent_map['entity_field_ids']
        field_id = field_name_id[name]
        value = entity_map['fields'][field_id]
        if field_id in entity_field_ids and isinstance(value, tuple):
            (extent_id, oid) = value
            EntityClass = self._entity_classes[extent_id]
            value = EntityClass(oid)
        return value

    def _entity_field_rev(self, extent_name, oid, name):
        """Return a tuple of (value, rev) of a field in an entity in
        named extent with given OID."""
        value = self._entity_field(extent_name, oid, name)
        rev = self._entity_rev(extent_name, oid)
        return (value, rev)

    def _entity_fields(self, extent_name, oid):
        """Return a dictionary of field values for an entity in
        `extent` with given OID."""
        entity_classes = self._entity_classes
        (entity_map, extent_map) = self._entity_extent_map(extent_name, oid)
        field_id_name = extent_map['field_id_name']
        entity_field_ids = extent_map['entity_field_ids']
        fields = {}
        for (field_id, value) in entity_map['fields'].iteritems():
            if field_id in entity_field_ids and isinstance(value, tuple):
                (extent_id, oid) = value
                EntityClass = entity_classes[extent_id]
                value = EntityClass(oid)
            field_name = field_id_name.get(field_id, None)
            if field_name:
                fields[field_name] = value

        return fields

    def _entity_links(self, extent_name, oid, other_extent_name=None, other_field_name=None, return_count=False):
        """Return dictionary of (extent_name, field_name): entity_list
        pairs, or list of linking entities if `other_extent_name` and
        `other_field_name` are supplied; return link count instead if
        `return_count` is True."""
        assert log(1, '_entity_links', extent_name, oid, other_extent_name, other_field_name, return_count)
        entity_classes = self._entity_classes
        entity_map = self._entity_map(extent_name, oid)
        entity_links = entity_map['links']
        extent_maps_by_id = self._extent_maps_by_id
        if other_extent_name is not None:
            if other_field_name is not None:
                other_extent_map = self._extent_map(other_extent_name)
                other_extent_id = other_extent_map['id']
                try:
                    other_field_id = other_extent_map['field_name_id'][other_field_name]
                except KeyError:
                    raise error.FieldDoesNotExist('Field %r does not exist in extent %r' % (other_field_name, other_extent_name))
                else:
                    key = (
                     other_extent_id, other_field_id)
                    btree = entity_links.get(key, {})
                    if return_count:
                        count = len(btree.keys())
                        assert log(2, 'returning len(btree.keys())', count)
                        return count
                    else:
                        EntityClass = entity_classes[other_extent_name]
                        others = [ EntityClass(oid) for oid in btree ]
                        return others
            link_count = entity_map['link_count']
            if return_count and other_extent_name is None:
                pass
            else:
                raise log(2, 'returning link_count', link_count) or AssertionError
            return link_count
        specific_extent_name = other_extent_name
        if return_count:
            links = 0
        else:
            links = {}
        if link_count == 0:
            assert log(2, 'no links - returning', links)
            return links
        for (key, btree) in entity_links.iteritems():
            (other_extent_id, other_field_id) = key
            other_extent_map = extent_maps_by_id[other_extent_id]
            other_extent_name = other_extent_map['name']
            if specific_extent_name:
                if specific_extent_name != other_extent_name:
                    pass
                else:
                    raise log(2, 'Skipping', other_extent_name) or AssertionError
                continue
            if return_count:
                links += len(btree.keys())
            else:
                other_field_name = other_extent_map['field_id_name'][other_field_id]
                if specific_extent_name:
                    link_key = other_field_name
                else:
                    link_key = (
                     other_extent_name, other_field_name)
                EntityClass = entity_classes[other_extent_name]
                others = [ EntityClass(oid) for oid in btree ]
                if others:
                    links[link_key] = others

        if return_count:
            assert log(2, 'returning links', links)
        return links

    def _entity_rev(self, extent_name, oid):
        """Return the revision of an entity in `extent` with given
        OID."""
        entity_map = self._entity_map(extent_name, oid)
        return entity_map['rev']

    def _extent_contains_oid(self, extent_name, oid):
        extent_map = self._extent_map(extent_name)
        return oid in extent_map['entities']

    def _extent_len(self, extent_name):
        """Return the number of entities in the named extent."""
        extent_map = self._extent_map(extent_name)
        return extent_map['len']

    def _extent_next_oid(self, extent_name):
        """Return the next OID to be assigned in the named extent."""
        extent_map = self._extent_map(extent_name)
        return extent_map['next_oid']

    def _find_entity_oids(self, extent_name, **criteria):
        """Return list of entity OIDs matching given field value(s)."""
        assert log(1, extent_name, criteria)
        extent_map = self._extent_map(extent_name)
        entity_maps = extent_map['entities']
        EntityClass = self._entity_classes[extent_name]
        if not criteria:
            assert log(2, 'Return all oids.')
            return entity_maps.keys()
        extent_name_id = self._extent_name_id
        indices = extent_map['indices']
        assert log(3, 'indices.keys()', indices.keys())
        normalized_index_map = extent_map['normalized_index_map']
        assert log(3, 'normalized_index_map.keys()', normalized_index_map.keys())
        entity_field_ids = extent_map['entity_field_ids']
        field_name_id = extent_map['field_name_id']
        field_id_value = {}
        field_spec = EntityClass._field_spec
        for (field_name, value) in criteria.iteritems():
            try:
                field_id = field_name_id[field_name]
            except KeyError:
                raise error.FieldDoesNotExist('Field %r does not exist for %r' % (field_name, extent_name))

            if field_id in entity_field_ids and isinstance(value, Entity):
                other_extent_id = extent_name_id[value._extent.name]
                other_oid = value._oid
                value = (other_extent_id, other_oid)
            else:
                FieldClass = field_spec[field_name]
                field = FieldClass(None, None)
                value = field.convert(value)
            field_id_value[field_id] = value

        field_ids = tuple(sorted(field_id_value))
        assert log(3, 'field_ids', field_ids)
        len_field_ids = len(field_ids)
        index_spec = None
        if field_ids in normalized_index_map:
            for spec in normalized_index_map[field_ids]:
                if len(spec) == len_field_ids:
                    index_spec = spec
                    break

        results = []
        if index_spec is not None:
            assert log(2, 'Use index spec:', index_spec)
            (unique, branch) = indices[index_spec]
            match = True
            for field_id in index_spec:
                field_value = field_id_value[field_id]
                if field_value not in branch:
                    assert log(3, field_value, 'not found in', branch.keys())
                    match = False
                    break
                branch = branch[field_value]

            if match:
                results = branch.keys()
        assert log(2, 'Use brute force.')
        append = results.append
        for (oid, entity_map) in entity_maps.iteritems():
            fields = entity_map['fields']
            match = True
            for (field_id, value) in field_id_value.iteritems():
                if fields[field_id] != value:
                    match = False
                    break

            if match:
                append(oid)

        assert log(2, 'Result count', len(results))
        return results

    def _relax_index(self, extent_name, *index_spec):
        """Relax constraints on the specified index until a matching
        enforce_index is called, or the currently-executing
        transaction finishes, whichever occurs first."""
        executing = self._executing
        if not executing:
            raise RuntimeError('Indexes can only be relaxed inside transaction execution.')
        extent_map = self._extent_map(extent_name)
        index_spec = _field_ids(extent_map, index_spec)
        indices = extent_map['indices']
        if index_spec not in indices:
            raise error.IndexDoesNotExist('Index %r not found in extent %r.' % (_field_names(extent_map, index_spec), extent_name))
        current_txn = executing[(-1)]
        relaxed = self._relaxed[extent_name]
        (txns, added) = relaxed.setdefault(index_spec, ([], []))
        txns.append(current_txn)
        current_txn._relaxed.add((extent_name, index_spec))

    def _set_extent_next_oid(self, extent_name, next_oid):
        extent_map = self._extent_map(extent_name)
        extent_map['next_oid'] = next_oid

    def _update_entity(self, extent_name, oid, fields, rev=None):
        """Update an existing entity in an extent."""
        entity_classes = self._entity_classes
        (entity_map, extent_map) = self._entity_extent_map(extent_name, oid)
        field_name_id = extent_map['field_name_id']
        entity_field_ids = extent_map['entity_field_ids']
        extent_name_id = self._extent_name_id
        extent_maps_by_id = self._extent_maps_by_id
        indices_added = []
        indices_removed = []
        new_links = []
        links_created = []
        links_deleted = []
        ia_append = indices_added.append
        ir_append = indices_removed.append
        nl_append = new_links.append
        lc_append = links_created.append
        ld_append = links_deleted.append
        try:
            old_fields = self._entity_fields(extent_name, oid)
            old_rev = entity_map['rev']
            for (name, value) in fields.items():
                field_id = field_name_id[name]
                if field_id in entity_field_ids and isinstance(value, Entity):
                    other_extent_id = extent_name_id[value._extent.name]
                    other_oid = value._oid
                    value = (other_extent_id, other_oid)
                    nl_append((field_id, other_extent_id, other_oid))
                fields[name] = value

            fields_by_id = entity_map['fields']
            all_field_ids = set(extent_map['field_id_name'].iterkeys())
            new_fields = all_field_ids - set(fields_by_id.iterkeys())
            fields_by_id.update(dict(((field_id, UNASSIGNED) for field_id in new_fields)))
            indices = extent_map['indices']
            for index_spec in indices.iterkeys():
                field_values = tuple((fields_by_id[field_id] for field_id in index_spec))
                relaxed_specs = self._relaxed[extent_name]
                if index_spec in relaxed_specs:
                    (txns, relaxed) = relaxed_specs[index_spec]
                else:
                    relaxed = None
                _index_remove(extent_map, index_spec, oid, field_values)
                ir_append((extent_map, index_spec, relaxed, oid, field_values))

            referrer_extent_id = extent_name_id[extent_name]
            for referrer_field_id in entity_field_ids:
                other_value = fields_by_id[referrer_field_id]
                if isinstance(other_value, tuple):
                    (other_extent_id, other_oid) = other_value
                    link_key = (referrer_extent_id, referrer_field_id)
                    other_extent_map = extent_maps_by_id[other_extent_id]
                    other_entity_map = other_extent_map['entities'][other_oid]
                    links = other_entity_map['links']
                    other_links = links[link_key]
                    del other_links[oid]
                    other_entity_map['link_count'] -= 1
                    ld_append((other_entity_map, links, link_key, oid))

            new_fields = dict(fields_by_id)
            for (name, value) in fields.iteritems():
                new_fields[field_name_id[name]] = value

            for index_spec in indices.iterkeys():
                field_values = tuple((new_fields[field_id] for field_id in index_spec))
                relaxed_specs = self._relaxed[extent_name]
                if index_spec in relaxed_specs:
                    (txns, relaxed) = relaxed_specs[index_spec]
                else:
                    relaxed = None
                _index_add(extent_map, index_spec, relaxed, oid, field_values)
                ia_append((extent_map, index_spec, oid, field_values))

            referrer_extent_id = extent_name_id[extent_name]
            for (referrer_field_id, other_extent_id, other_oid) in new_links:
                other_extent_map = extent_maps_by_id[other_extent_id]
                try:
                    other_entity_map = other_extent_map['entities'][other_oid]
                except KeyError:
                    field_id_name = extent_map['field_id_name']
                    field_name = field_id_name[referrer_field_id]
                    raise error.EntityDoesNotExist('Entity referenced in %r does not exist.' % field_name)

                links = other_entity_map['links']
                link_key = (referrer_extent_id, referrer_field_id)
                if link_key not in links:
                    links[link_key] = BTree()
                links[link_key][oid] = None
                other_entity_map['link_count'] += 1
                lc_append((other_entity_map, links, link_key, oid))

            for (name, value) in fields.iteritems():
                fields_by_id[field_name_id[name]] = value

            if rev is None:
                entity_map['rev'] += 1
            else:
                entity_map['rev'] = rev
            self._append_inversion(self._update_entity, extent_name, oid, old_fields, old_rev)
            append_change = self._append_change
            append_change(UPDATE, extent_name, oid)
        except:
            for (_e, _i, _o, _f) in indices_added:
                _index_remove(_e, _i, _o, _f)

            for (_e, _i, _r, _o, _f) in indices_removed:
                _index_add(_e, _i, _r, _o, _f)

            for (other_entity_map, links, link_key, oid) in links_created:
                del links[link_key][oid]
                other_entity_map['link_count'] -= 1

            for (other_entity_map, links, link_key, oid) in links_deleted:
                links[link_key][oid] = None
                other_entity_map['link_count'] += 1

            raise

        return

    def _create_extent(self, extent_name, field_names, entity_field_names, key_spec=None, index_spec=None):
        """Create a new extent with a given name."""
        if extent_name in self._extent_maps_by_name:
            raise error.ExtentExists('%r already exists.' % extent_name)
        if key_spec is None:
            key_spec = []
        if index_spec is None:
            index_spec = []
        extent_map = PDict()
        extent_id = self._unique_extent_id()
        indices = extent_map['indices'] = PDict()
        extent_map['index_map'] = PDict()
        normalized_index_map = extent_map['normalized_index_map'] = PDict()
        extent_map['entities'] = BTree()
        field_id_name = extent_map['field_id_name'] = PDict()
        field_name_id = extent_map['field_name_id'] = PDict()
        extent_map['id'] = extent_id
        extent_map['len'] = 0
        extent_map['name'] = extent_name
        extent_map['next_oid'] = 1
        self._extent_name_id[extent_name] = extent_id
        self._extent_maps_by_id[extent_id] = extent_map
        self._extent_maps_by_name[extent_name] = extent_map
        for name in field_names:
            field_id = self._unique_field_id(extent_name)
            field_id_name[field_id] = name
            field_name_id[name] = field_id

        for field_names in key_spec:
            i_spec = _field_ids(extent_map, field_names)
            _create_index(extent_map, i_spec, True)

        for field_names in index_spec:
            i_spec = _field_ids(extent_map, field_names)
            _create_index(extent_map, i_spec, False)

        extent_map['entity_field_ids'] = _field_ids(extent_map, entity_field_names)
        return

    def _delete_extent(self, extent_name):
        """Remove a named extent."""
        extent_map = self._extent_map(extent_name)
        extent_id = extent_map['id']
        del self._extent_name_id[extent_name]
        del self._extent_maps_by_id[extent_id]
        del self._extent_maps_by_name[extent_name]

    def _create_schevo_structures(self):
        """Create or update Schevo structures in the database."""
        root = self._root
        if 'SCHEVO' not in root.keys():
            schevo = root['SCHEVO'] = PDict()
            schevo['format'] = 1
            schevo['version'] = 0
            schevo['extent_name_id'] = PDict()
            schevo['extents'] = PDict()
            schevo['schema_source'] = None
        return

    def _entity_map(self, extent_name, oid):
        """Return an entity PDict corresponding to named
        `extent` and OID."""
        extent_map = self._extent_map(extent_name)
        try:
            entity_map = extent_map['entities'][oid]
        except KeyError:
            raise error.EntityDoesNotExist('OID %r does not exist in %r' % (oid, extent_name))

        return entity_map

    def _entity_extent_map(self, extent_name, oid):
        """Return an (entity PDict, extent PDict)
        tuple corresponding to named `extent` and OID."""
        extent_map = self._extent_map(extent_name)
        try:
            entity_map = extent_map['entities'][oid]
        except KeyError:
            raise error.EntityDoesNotExist('OID %r does not exist in %r' % (oid, extent_name))

        return (entity_map, extent_map)

    def _evolve(self, schema_source, version):
        """Evolve the database to a new schema definition.

        - `schema_source`: String containing the source code for the
          schema to be evolved to.

        - `version`: Integer with the version number of the new schema
          source.  Must be the current database version, plus 1.
        """
        if version != self.version + 1:
            raise error.DatabaseVersionMismatch('Current version is %i, expected %i, got %i' % (self.version, self.version + 1, version))

        def call(module, name):
            fn = getattr(module, name, None)
            if callable(fn):
                tx = CallableWrapper(fn)
                self._executing = [
                 Transaction()]
                try:
                    self.execute(tx)
                finally:
                    self._executing = []
            return

        schema_name = schema_counter.next_schema_name()
        schema_module = self._import_from_source(schema_source, schema_name)
        try:
            call(schema_module, 'before_evolve')
            self._sync(schema_source, initialize=False, commit=False, evolving=True)
            call(self._schema_module, 'during_evolve')
            self._sync(schema_source, initialize=False, commit=False, evolving=False)
            call(self._schema_module, 'after_evolve')
        except:
            self._rollback()
            raise
        else:
            self._root['SCHEVO']['version'] = version
            self._commit()

    def _extent_map(self, extent_name):
        """Return an extent PDict corresponding to `extent_name`."""
        try:
            return self._extent_maps_by_name[extent_name]
        except KeyError:
            raise error.ExtentDoesNotExist('%r does not exist.' % extent_name)

    def _import_from_source(self, source, module_name):
        """Import a schema module from a string containing source code."""
        schema_module = module.from_string(source, module_name)
        module.remember(schema_module)
        self._remembered.append(schema_module)
        schema_module.db = self
        return schema_module

    def _initialize(self):
        """Populate the database with initial data."""
        tx = Initialize()
        self.execute(tx)

    def _on_open(self):
        """Allow schema to run code after the database is opened."""
        if hasattr(self, '_schema_module'):
            fn = getattr(self._schema_module, 'on_open', None)
            if callable(fn):
                fn(self)
        return

    def _remove_stale_links(self, extent_id, field_id, FieldClass):
        allow = FieldClass.allow
        for other_name in allow:
            other_extent_map = self._extent_map(other_name)
            other_entities = other_extent_map['entities']
            for other_entity in other_entities.itervalues():
                other_link_count = other_entity['link_count']
                other_links = other_entity['links']
                referrer_key = (extent_id, field_id)
                if referrer_key in other_links:
                    referrers = other_links[referrer_key]
                    other_link_count -= len(referrers.keys())
                    del other_links[referrer_key]
                other_entity['link_count'] = other_link_count

    def _sync(self, schema_source=None, initialize=True, commit=True, evolving=False):
        """Synchronize the database with a schema definition.

        - `schema_source`: String containing the source code for a
          schema.  If `None`, the schema source contained in the
          database itself will be used.

        - `initialize`: True if a new database should be populated
          with initial values defined in the schema.

        - `commit`: True if a successful synchronization should commit
          to the storage backend.  False if the caller of `_sync` will
          handle this task.

        - `evolving`: True if the synchronization is occuring during a
          database evolution.
        """
        sync_schema_changes = True
        locked = False
        try:
            SCHEVO = self._root['SCHEVO']
            old_schema_source = SCHEVO['schema_source']
            if old_schema_source is not None:
                old_schema_module = None
                schevo.schema.start(self, evolving)
                locked = True
                schema_name = schema_counter.next_schema_name()
                try:
                    old_schema_module = self._import_from_source(old_schema_source, schema_name)
                finally:
                    old_schema = schevo.schema.finish(self, old_schema_module)
                    locked = False
                self._old_schema = old_schema
                self._old_schema_module = old_schema_module
            else:
                old_schema = self._old_schema = None
                old_schema_module = self._old_schema_module = None
            if schema_source is None:
                schema_source = old_schema_source
                if schema_source is None:
                    return
                else:
                    sync_schema_changes = False
            if schema_source == old_schema_source:
                schema = old_schema
                schema_module = old_schema_module
            else:
                schema_source = schema_source.replace('from schevo import *\nfrom schevo.namespace import schema_prep\nschema_prep(locals())\n', 'from schevo.schema import *\nschevo.schema.prep(locals())\n')
                schema_module = None
                schevo.schema.start(self, evolving)
                locked = True
                schema_name = schema_counter.next_schema_name()
                try:
                    schema_module = self._import_from_source(schema_source, schema_name)
                finally:
                    schema = schevo.schema.finish(self, schema_module)
                    locked = False
            self.schema = schema
            self._schema_module = schema_module
            self.q = schema.q
            self.t = schema.t
            self.Q = schema.Q
            self.x = DatabaseExtenders(self._schema_module)
            if sync_schema_changes:
                SCHEVO['schema_source'] = schema_source
                self._sync_extents(schema, evolving)
            E = schema.E
            extents = self._extents = {}
            relaxed = self._relaxed = {}
            entity_classes = self._entity_classes = {}
            extent_name_id = self._extent_name_id
            for e_name in self.extent_names():
                e_id = extent_name_id[e_name]
                EntityClass = E[e_name]
                extent = Extent(self, e_name, EntityClass)
                extents[e_id] = extents[e_name] = extent
                relaxed[e_name] = {}
                entity_classes[e_id] = entity_classes[e_name] = EntityClass
                setattr(self, e_name, extent)

            if SCHEVO['version'] == 0:
                SCHEVO['version'] = 1
                if initialize:
                    self._initialize()
        except:
            if locked:
                schevo.schema.import_lock.release()
            if commit:
                self._rollback()
            raise
        else:
            if commit:
                self._commit()

        return

    def _sync_extents(self, schema, evolving):
        """Synchronize the extents based on the schema."""
        E = schema.E
        old_schema = self._old_schema
        in_schema = set(iter(E))
        if evolving:
            for extent_name in in_schema:
                EntityClass = E[extent_name]
                was_named = EntityClass._was
                if was_named is not None:
                    extent_name_id = self._extent_name_id
                    extent_map = self._extent_map(was_named)
                    extent_id = extent_map['id']
                    extent_map['name'] = extent_name
                    del extent_name_id[was_named]
                    extent_name_id[extent_name] = extent_id

            self._update_extent_maps_by_name()
        in_db = set(self.extent_names())
        to_create = in_schema - in_db
        for extent_name in to_create:
            if extent_name.startswith('_'):
                continue
            EntityClass = E[extent_name]
            field_spec = EntityClass._field_spec
            field_names = field_spec.keys()
            entity_field_names = []
            for name in field_names:
                if issubclass(field_spec[name], EntityField):
                    entity_field_names.append(name)

            key_spec = EntityClass._key_spec
            index_spec = EntityClass._index_spec
            self._create_extent(extent_name, field_names, entity_field_names, key_spec, index_spec)

        in_db = set(self.extent_names())
        to_remove = in_db - in_schema
        for extent_name in to_remove:
            if extent_name.startswith('_'):
                continue
            if old_schema:
                extent_map = self._extent_map(extent_name)
                field_name_id = extent_map['field_name_id']
                extent_id = extent_map['id']
                if extent_name in old_schema.E:
                    for (old_field_name, FieldClass) in old_schema.E[extent_name]._field_spec.iteritems():
                        old_field_id = field_name_id[old_field_name]
                        if issubclass(FieldClass, EntityField):
                            self._remove_stale_links(extent_id, old_field_id, FieldClass)

            self._delete_extent(extent_name)

        for extent_name in self.extent_names():
            EntityClass = E[extent_name]
            field_spec = EntityClass._field_spec
            extent_map = self._extent_map(extent_name)
            extent_id = extent_map['id']
            entity_field_ids = set(extent_map['entity_field_ids'])
            field_id_name = extent_map['field_id_name']
            field_name_id = extent_map['field_name_id']
            existing_field_names = set(field_name_id.keys())
            new_field_names = set(field_spec.keys())
            if evolving:
                for field_name in new_field_names:
                    field_class = field_spec[field_name]
                    was_named = field_class.was
                    if was_named is not None:
                        if was_named not in existing_field_names:
                            raise error.FieldDoesNotExist('Field %s.%s was being renamed from %s, but that field does not exist in the previous schema.' % (extent_name, field_name, was_named))
                        field_id = field_name_id[was_named]
                        del field_name_id[was_named]
                        field_name_id[field_name] = field_id
                        field_id_name[field_id] = field_name
                        existing_field_names.remove(was_named)

            old_field_names = existing_field_names - new_field_names
            for old_field_name in old_field_names:
                old_field_id = field_name_id[old_field_name]
                if old_schema:
                    if extent_name in old_schema.E:
                        FieldClass = old_schema.E[extent_name]._field_spec.get(old_field_name, None)
                        if FieldClass is not None and issubclass(FieldClass, EntityField):
                            self._remove_stale_links(extent_id, old_field_id, FieldClass)
                if old_field_id in entity_field_ids:
                    entity_field_ids.remove(old_field_id)
                del field_name_id[old_field_name]
                del field_id_name[old_field_id]

            existing_field_names = set(field_name_id.keys())
            fields_to_create = new_field_names - existing_field_names
            for field_name in fields_to_create:
                field_id = self._unique_field_id(extent_name)
                field_name_id[field_name] = field_id
                field_id_name[field_id] = field_name
                if issubclass(field_spec[field_name], EntityField):
                    entity_field_ids.add(field_id)

            extent_map['entity_field_ids'] = tuple(entity_field_ids)

        for extent_name in self.extent_names():
            EntityClass = E[extent_name]
            key_spec = EntityClass._key_spec
            index_spec = EntityClass._index_spec
            self._update_extent_key_spec(extent_name, key_spec, index_spec)

        return

    def _unique_extent_id(self):
        """Return an unused random extent ID."""
        extent_name_id = self._extent_name_id
        while True:
            extent_id = random.randint(0, 2 ** 31)
            if extent_id not in extent_name_id:
                return extent_id

    def _unique_field_id(self, extent_name):
        """Return an unused random field ID."""
        field_id_name = self._extent_map(extent_name)['field_id_name']
        while True:
            field_id = random.randint(0, 2 ** 31)
            if field_id not in field_id_name:
                return field_id

    def _update_extent_maps_by_name(self):
        extent_maps_by_name = self._extent_maps_by_name = {}
        for extent in self._extent_maps_by_id.itervalues():
            extent_maps_by_name[extent['name']] = extent

    def _update_extent_key_spec(self, extent_name, key_spec, index_spec):
        """Update an existing extent to match given key spec."""
        extent_map = self._extent_map(extent_name)
        entities = extent_map['entities']
        indices = extent_map['indices']
        key_spec_ids = [ _field_ids(extent_map, field_names) for field_names in key_spec ]
        index_spec_ids = [ _field_ids(extent_map, field_names) for field_names in index_spec ]
        for i_spec in index_spec_ids:
            if i_spec not in key_spec and i_spec in indices:
                (unique, branch) = indices[i_spec]
                indices[i_spec] = (False, branch)

        for i_spec in key_spec_ids:
            if i_spec not in indices:
                _create_index(extent_map, i_spec, True)
                for oid in entities:
                    fields_by_id = entities[oid]['fields']
                    field_values = tuple((fields_by_id.get(field_id, UNASSIGNED) for field_id in i_spec))
                    _index_add(extent_map, i_spec, None, oid, field_values)

        for i_spec in index_spec_ids:
            if i_spec not in indices:
                _create_index(extent_map, i_spec, False)
                for oid in entities:
                    fields_by_id = entities[oid]['fields']
                    field_values = tuple((fields_by_id.get(field_id, UNASSIGNED) for field_id in i_spec))
                    _index_add(extent_map, i_spec, None, oid, field_values)

        to_remove = set(indices.keys()) - set(key_spec_ids + index_spec_ids)
        for i_spec in to_remove:
            _delete_index(extent_map, i_spec)

        for (i_spec, (unique, branch)) in indices.items():
            if not unique:
                spec_set = set(index_spec)
                for i_spec in indices:
                    compare_set = set(i_spec)
                    if compare_set.issuperset(spec_set):
                        unique = True
                        break

                if unique:
                    indices[i_spec] = (unique, branch)
                    for oid in entities:
                        fields_by_id = entities[oid]['fields']
                        field_values = tuple((fields_by_id[field_id] for field_id in i_spec))
                        _index_validate(extent_map, i_spec, oid, field_values)

        return

    def _validate_changes(self, changes):
        entity_classes = self._entity_classes
        changes = change.normalize(changes)
        for (typ, extent_name, oid) in changes:
            if typ in (CREATE, UPDATE):
                EntityClass = entity_classes[extent_name]
                entity = EntityClass(oid)
                field_map = entity.sys.field_map(not_fget)
                for field in field_map.itervalues():
                    field.validate(field._value)

    def _reset_all(self):
        """Clear all entities, indices, etc. in the database.

        FOR USE WITH SINGLE-SCHEMA UNIT TESTS.

        NOT INDENDED FOR GENERAL USE.
        """
        for extent_name in self.extent_names():
            extent_map = self._extent_map(extent_name)
            extent_map['entities'] = BTree()
            extent_map['len'] = 0
            extent_map['next_oid'] = 1
            indices = extent_map['indices']
            for (index_spec, (unique, index_tree)) in indices.items():
                indices[index_spec] = (
                 unique, BTree())

        self._commit()
        self.dispatch = Database.dispatch
        self.label = Database.label
        self._initialize()
        self._on_open()


def _create_index(extent_map, index_spec, unique):
    """Create a new index in the extent with the given spec and
    uniqueness flag."""
    assert log(1, extent_map['name'])
    assert log(1, 'index_spec', index_spec)
    indices = extent_map['indices']
    index_map = extent_map['index_map']
    normalized_index_map = extent_map['normalized_index_map']
    if not unique:
        spec_set = set(index_spec)
        for i_spec in indices:
            compare_set = set(i_spec)
            if compare_set.issubset(spec_set):
                unique = True
                break

    assert log(2, 'unique', unique)
    assert log(2, 'normalized_index_map.keys()', normalized_index_map.keys())
    partial_specs = _partial_index_specs(index_spec)
    assert log(3, 'partial_specs', partial_specs)
    normalized_specs = _normalized_index_specs(partial_specs)
    assert log(3, 'normalized_specs', normalized_specs)
    index_root = BTree()
    indices[index_spec] = (unique, index_root)
    for partial_spec in partial_specs:
        L = index_map.setdefault(partial_spec, PList())
        L.append(index_spec)

    for normalized_spec in normalized_specs:
        L = normalized_index_map.setdefault(normalized_spec, PList())
        L.append(index_spec)

    assert log(2, 'normalized_index_map.keys()', normalized_index_map.keys())


def _delete_index(extent_map, index_spec):
    indices = extent_map['indices']
    index_map = extent_map['index_map']
    normalized_index_map = extent_map['normalized_index_map']
    partial_specs = _partial_index_specs(index_spec)
    normalized_specs = _normalized_index_specs(partial_specs)
    del indices[index_spec]
    for partial_spec in partial_specs:
        L = index_map[partial_spec]
        L.remove(index_spec)
        if not L:
            del index_map[partial_spec]

    for normalized_spec in normalized_specs:
        if normalized_spec in normalized_index_map:
            L = normalized_index_map[normalized_spec]
            L.remove(index_spec)
            if not L:
                del normalized_index_map[normalized_spec]


def _field_ids(extent_map, field_names):
    """Convert a (field-name, ...) tuple to a (field-id, ...)
    tuple for the given extent map."""
    field_name_id = extent_map['field_name_id']
    return tuple((field_name_id[name] for name in field_names))


def _field_names(extent_map, field_ids):
    """Convert a (field-id, ...) tuple to a (field-name, ...) tuple
    for the given extent map."""
    field_id_name = extent_map['field_id_name']
    return tuple((field_id_name[id] for id in field_ids))


def _index_add(extent_map, index_spec, relaxed, oid, field_values):
    """Add an entry to the specified index, of entity oid having the
    given values in order of the index spec."""
    indices = extent_map['indices']
    (unique, branch) = indices[index_spec]
    for (field_id, field_value) in zip(index_spec, field_values):
        if field_value in branch:
            branch = branch[field_value]
        else:
            new_branch = BTree()
            branch[field_value] = new_branch
            branch = new_branch

    if unique and branch.keys() and relaxed is None:
        _index_clean(extent_map, index_spec, field_values)
        raise error.KeyCollision('Duplicate value %r for key %r on %r' % (field_values, _field_names(extent_map, index_spec), extent_map['name']), branch.keys()[0])
    branch[oid] = True
    if relaxed is not None:
        relaxed.append((extent_map, index_spec, oid, field_values))
    return


def _index_clean(extent_map, index_spec, field_values):
    """Remove stale branches from the specified index."""
    indices = extent_map['indices']
    (unique, branch) = indices[index_spec]
    _index_clean_branch(branch, field_values)


def _index_clean_branch(branch, field_values):
    """Recursively clean a branch of stale child branches."""
    branch_value = field_values[0]
    child_values = field_values[1:]
    if branch_value in branch:
        if child_values:
            _index_clean_branch(branch[branch_value], child_values)
        if not branch[branch_value].keys():
            del branch[branch_value]


def _index_remove(extent_map, index_spec, oid, field_values):
    """Remove an entry from the specified index, of entity oid having
    the given values in order of the index spec."""
    indices = extent_map['indices']
    (unique, branch) = indices[index_spec]
    for (field_id, field_value) in zip(index_spec, field_values):
        if field_value not in branch:
            break
        branch = branch[field_value]

    if oid in branch:
        del branch[oid]
    _index_clean(extent_map, index_spec, field_values)


def _index_validate(extent_map, index_spec, oid, field_values):
    """Validate the index entry for uniqueness."""
    indices = extent_map['indices']
    (unique, branch) = indices[index_spec]
    for (field_id, field_value) in zip(index_spec, field_values):
        if field_value in branch:
            branch = branch[field_value]
        else:
            new_branch = BTree()
            branch[field_value] = new_branch
            branch = new_branch

    if unique and len(branch.keys()) > 1:
        _index_clean(extent_map, index_spec, field_values)
        raise error.KeyCollision('Duplicate value %r for key %r' % (field_values, _field_names(extent_map, index_spec)), None)
    return


def _normalized_index_specs(index_specs):
    """Return normalized index specs based on index_specs."""
    return [ tuple(sorted(spec)) for spec in index_specs ]


def _partial_index_specs(index_spec):
    """Return a list of partial index specs based on index_spec."""
    return [ tuple(index_spec[:x + 1]) for x in xrange(len(index_spec)) ]


def _walk_index(branch, ascending_seq, result_list):
    """Recursively walk a branch of an index, appending OIDs found to
    result_list.

    - `branch`: The branch to start at.
    - `ascending_seq`: The sequence of ascending flags corresponding
      to the current branch.
    - `result_list`: List to append OIDs to.
    """
    if len(ascending_seq):
        ascending, inner_ascending = ascending_seq[0], ascending_seq[1:]
        if ascending:
            for (key, inner_branch) in branch.iteritems():
                _walk_index(inner_branch, inner_ascending, result_list)

        else:
            keys = reversed(branch.keys())
            for key in keys:
                inner_branch = branch[key]
                _walk_index(inner_branch, inner_ascending, result_list)

    else:
        result_list.extend(branch.iterkeys())


class DatabaseExtenders(NamespaceExtension):
    """Methods that extend the functionality of a database."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__
    _readonly = False

    def __init__(self, schema_module):
        NamespaceExtension.__init__(self)
        for name in dir(schema_module):
            if name.startswith('x_'):
                function = getattr(schema_module, name)
                name = name[2:]
                self._set(name, function)


optimize.bind_all(sys.modules[__name__])