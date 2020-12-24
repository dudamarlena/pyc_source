# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/creator/changes.py
# Compiled at: 2018-07-11 18:15:31
"""
Contains things to detect changes - either using options passed in on the
commandline, or by using autodetection, etc.
"""
from __future__ import print_function
from django.db import models
from django.contrib.contenttypes.generic import GenericRelation
from django.utils.datastructures import SortedDict
from south.creator.freezer import remove_useless_attributes, freeze_apps, model_key
from south.utils import auto_through
from south.utils.py3 import string_types

class BaseChanges(object):
    """
    Base changes class.
    """

    def suggest_name(self):
        return ''

    def split_model_def(self, model, model_def):
        """
        Given a model and its model def (a dict of field: triple), returns three
        items: the real fields dict, the Meta dict, and the M2M fields dict.
        """
        real_fields = SortedDict()
        meta = SortedDict()
        m2m_fields = SortedDict()
        for name, triple in model_def.items():
            if name == 'Meta':
                meta = triple
            elif isinstance(model._meta.get_field_by_name(name)[0], models.ManyToManyField):
                m2m_fields[name] = triple
            else:
                real_fields[name] = triple

        return (
         real_fields, meta, m2m_fields)

    def current_model_from_key(self, key):
        app_label, model_name = key.split('.')
        return models.get_model(app_label, model_name)

    def current_field_from_key(self, key, fieldname):
        app_label, model_name = key.split('.')
        if fieldname == '_order':
            field = models.IntegerField()
            field.name = '_order'
            field.attname = '_order'
            field.column = '_order'
            field.default = 0
            return field
        return models.get_model(app_label, model_name)._meta.get_field_by_name(fieldname)[0]


class AutoChanges(BaseChanges):
    """
    Detects changes by 'diffing' two sets of frozen model definitions.
    """
    IGNORED_FIELD_TYPES = [
     GenericRelation]

    def __init__(self, migrations, old_defs, old_orm, new_defs):
        self.migrations = migrations
        self.old_defs = old_defs
        self.old_orm = old_orm
        self.new_defs = new_defs

    def suggest_name(self):
        parts = [
         'auto']
        for change_name, params in self.get_changes():
            if change_name == 'AddModel':
                parts.append('add_%s' % params['model']._meta.object_name.lower())
            elif change_name == 'DeleteModel':
                parts.append('del_%s' % params['model']._meta.object_name.lower())
            elif change_name == 'AddField':
                parts.append('add_field_%s_%s' % (
                 params['model']._meta.object_name.lower(),
                 params['field'].name))
            elif change_name == 'DeleteField':
                parts.append('del_field_%s_%s' % (
                 params['model']._meta.object_name.lower(),
                 params['field'].name))
            elif change_name == 'ChangeField':
                parts.append('chg_field_%s_%s' % (
                 params['model']._meta.object_name.lower(),
                 params['new_field'].name))
            elif change_name == 'AddUnique':
                parts.append('add_unique_%s_%s' % (
                 params['model']._meta.object_name.lower(),
                 ('_').join([ x.name for x in params['fields'] ])))
            elif change_name == 'DeleteUnique':
                parts.append('del_unique_%s_%s' % (
                 params['model']._meta.object_name.lower(),
                 ('_').join([ x.name for x in params['fields'] ])))
            elif change_name == 'AddIndex':
                parts.append('add_index_%s_%s' % (
                 params['model']._meta.object_name.lower(),
                 ('_').join([ x.name for x in params['fields'] ])))
            elif change_name == 'DeleteIndex':
                parts.append('del_index_%s_%s' % (
                 params['model']._meta.object_name.lower(),
                 ('_').join([ x.name for x in params['fields'] ])))

        return ('__').join(parts)[:70]

    def get_changes(self):
        """
        Returns the difference between the old and new sets of models as a 5-tuple:
        added_models, deleted_models, added_fields, deleted_fields, changed_fields
        """
        deleted_models = set()
        for key in self.old_defs:
            if key not in self.new_defs:
                old_fields, old_meta, old_m2ms = self.split_model_def(self.old_orm[key], self.old_defs[key])
                if old_meta.get('managed', 'True') != 'False':
                    yield ('DeleteModel',
                     {'model': self.old_orm[key], 
                        'model_def': old_fields})
                    for fieldname in old_m2ms:
                        field = self.old_orm[(key + ':' + fieldname)]
                        if auto_through(field):
                            yield (
                             'DeleteM2M', {'model': self.old_orm[key], 'field': field})

                    for attr, operation in (('unique_together', 'DeleteUnique'), ('index_together', 'DeleteIndex')):
                        together = eval(old_meta.get(attr, '[]'))
                        if together:
                            if isinstance(together[0], string_types):
                                together = [
                                 together]
                            for fields in together:
                                yield (
                                 operation,
                                 {'model': self.old_orm[key], 
                                    'fields': [ self.old_orm[key]._meta.get_field_by_name(x)[0] for x in fields ]})

                deleted_models.add(key)

        for key in self.new_defs:
            if key not in self.old_defs:
                new_fields, new_meta, new_m2ms = self.split_model_def(self.current_model_from_key(key), self.new_defs[key])
                if new_meta.get('managed', 'True') != 'False':
                    yield (
                     'AddModel',
                     {'model': self.current_model_from_key(key), 
                        'model_def': new_fields})
                    for fieldname in new_m2ms:
                        field = self.current_field_from_key(key, fieldname)
                        if auto_through(field):
                            yield (
                             'AddM2M', {'model': self.current_model_from_key(key), 'field': field})

                    for attr, operation in (('unique_together', 'AddUnique'), ('index_together', 'AddIndex')):
                        together = eval(new_meta.get(attr, '[]'))
                        if together:
                            if isinstance(together[0], string_types):
                                together = [
                                 together]
                            for fields in together:
                                yield (
                                 operation,
                                 {'model': self.current_model_from_key(key), 
                                    'fields': [ self.current_model_from_key(key)._meta.get_field_by_name(x)[0] for x in fields ]})

        for key in self.old_defs:
            if key not in deleted_models:
                old_fields, old_meta, old_m2ms = self.split_model_def(self.old_orm[key], self.old_defs[key])
                new_fields, new_meta, new_m2ms = self.split_model_def(self.current_model_from_key(key), self.new_defs[key])
                if new_meta.get('managed', 'True') == 'False':
                    continue
                for fieldname in old_fields:
                    if fieldname not in new_fields:
                        field = self.old_orm[(key + ':' + fieldname)]
                        field_allowed = True
                        for field_type in self.IGNORED_FIELD_TYPES:
                            if isinstance(field, field_type):
                                field_allowed = False

                        if field_allowed:
                            yield ('DeleteField',
                             {'model': self.old_orm[key], 
                                'field': field, 
                                'field_def': old_fields[fieldname]})

                for fieldname in new_fields:
                    if fieldname not in old_fields:
                        field = self.current_field_from_key(key, fieldname)
                        field_allowed = True
                        for field_type in self.IGNORED_FIELD_TYPES:
                            if isinstance(field, field_type):
                                field_allowed = False

                        if field_allowed:
                            yield ('AddField',
                             {'model': self.current_model_from_key(key), 
                                'field': field, 
                                'field_def': new_fields[fieldname]})

                for fieldname in old_m2ms:
                    if fieldname not in new_m2ms:
                        field = self.old_orm[(key + ':' + fieldname)]
                        if auto_through(field):
                            yield (
                             'DeleteM2M', {'model': self.old_orm[key], 'field': field})

                for fieldname in new_m2ms:
                    if fieldname not in old_m2ms:
                        field = self.current_field_from_key(key, fieldname)
                        if auto_through(field):
                            yield (
                             'AddM2M', {'model': self.current_model_from_key(key), 'field': field})

                for fieldname in set(old_fields).intersection(set(new_fields)):
                    if self.different_attributes(remove_useless_attributes(old_fields[fieldname], True, True), remove_useless_attributes(new_fields[fieldname], True, True)):
                        yield (
                         'ChangeField',
                         {'model': self.current_model_from_key(key), 
                            'old_field': self.old_orm[(key + ':' + fieldname)], 
                            'new_field': self.current_field_from_key(key, fieldname), 
                            'old_def': old_fields[fieldname], 
                            'new_def': new_fields[fieldname]})
                    old_field = self.old_orm[(key + ':' + fieldname)]
                    new_field = self.current_field_from_key(key, fieldname)
                    if not old_field.db_index and new_field.db_index:
                        yield ('AddIndex',
                         {'model': self.current_model_from_key(key), 
                            'fields': [
                                     new_field]})
                    if old_field.db_index and not new_field.db_index:
                        yield ('DeleteIndex',
                         {'model': self.old_orm[key], 
                            'fields': [
                                     old_field]})
                    if old_field.unique != new_field.unique:
                        if new_field.unique:
                            yield (
                             'AddUnique',
                             {'model': self.current_model_from_key(key), 
                                'fields': [
                                         new_field]})
                        else:
                            yield (
                             'DeleteUnique',
                             {'model': self.old_orm[key], 
                                'fields': [
                                         old_field]})

                for fieldname in set(old_m2ms).intersection(set(new_m2ms)):
                    old_field = self.old_orm[(key + ':' + fieldname)]
                    new_field = self.current_field_from_key(key, fieldname)
                    if auto_through(old_field) and not auto_through(new_field):
                        yield (
                         'DeleteM2M', {'model': self.old_orm[key], 'field': old_field})
                    if not auto_through(old_field) and auto_through(new_field):
                        yield (
                         'AddM2M', {'model': self.current_model_from_key(key), 'field': new_field})

                for attr, add_operation, del_operation in (('unique_together', 'AddUnique', 'DeleteUnique'), ('index_together', 'AddIndex', 'DeleteIndex')):
                    old_together = eval(old_meta.get(attr, '[]'))
                    new_together = eval(new_meta.get(attr, '[]'))
                    if old_together and isinstance(old_together[0], string_types):
                        old_together = [
                         old_together]
                    if new_together and isinstance(new_together[0], string_types):
                        new_together = [
                         new_together]
                    old_together = frozenset(tuple(o) for o in old_together)
                    new_together = frozenset(tuple(n) for n in new_together)
                    disappeared = old_together.difference(new_together)
                    appeared = new_together.difference(old_together)
                    for item in disappeared:
                        yield (
                         del_operation,
                         {'model': self.old_orm[key], 
                            'fields': [ self.old_orm[(key + ':' + x)] for x in item ]})

                    for item in appeared:
                        yield (add_operation,
                         {'model': self.current_model_from_key(key), 
                            'fields': [ self.current_field_from_key(key, x) for x in item ]})

    @classmethod
    def is_triple(cls, triple):
        """Returns whether the argument is a triple."""
        return isinstance(triple, (list, tuple)) and len(triple) == 3 and isinstance(triple[0], string_types) and isinstance(triple[1], (list, tuple)) and isinstance(triple[2], dict)

    @classmethod
    def different_attributes(cls, old, new):
        """
        Backwards-compat comparison that ignores orm. on the RHS and not the left
        and which knows django.db.models.fields.CharField = models.CharField.
        Has a whole load of tests in tests/autodetection.py.
        """
        if not cls.is_triple(old) or not cls.is_triple(new):
            return old != new
        old_field, old_pos, old_kwd = old
        new_field, new_pos, new_kwd = new
        old_pos, new_pos = old_pos[:], new_pos[:]
        old_kwd = dict(old_kwd.items())
        new_kwd = dict(new_kwd.items())
        if 'unique' in old_kwd:
            del old_kwd['unique']
        if 'unique' in new_kwd:
            del new_kwd['unique']
        if old_field != new_field:
            if old_field.startswith('models.') and (new_field.startswith('django.db.models') or new_field.startswith('django.contrib.gis')):
                if old_field.split('.')[(-1)] != new_field.split('.')[(-1)]:
                    return True
                old_field = new_field = ''
        if old_pos and 'to' in new_kwd and 'orm' in new_kwd['to'] and 'orm' not in old_pos[0]:
            try:
                if old_pos[0] != new_kwd['to'].split("'")[1].split('.')[1]:
                    return True
            except IndexError:
                pass

            old_pos = old_pos[1:]
            del new_kwd['to']
        return old_field != new_field or old_pos != new_pos or old_kwd != new_kwd


class ManualChanges(BaseChanges):
    """
    Detects changes by reading the command line.
    """

    def __init__(self, migrations, added_models, added_fields, added_indexes):
        self.migrations = migrations
        self.added_models = added_models
        self.added_fields = added_fields
        self.added_indexes = added_indexes

    def suggest_name(self):
        bits = []
        for model_name in self.added_models:
            bits.append('add_model_%s' % model_name)

        for field_name in self.added_fields:
            bits.append('add_field_%s' % field_name)

        for index_name in self.added_indexes:
            bits.append('add_index_%s' % index_name)

        return ('_').join(bits).replace('.', '_')

    def get_changes(self):
        model_defs = freeze_apps([self.migrations.app_label()])
        for model_name in self.added_models:
            model = models.get_model(self.migrations.app_label(), model_name)
            real_fields, meta, m2m_fields = self.split_model_def(model, model_defs[model_key(model)])
            yield ('AddModel',
             {'model': model, 
                'model_def': real_fields})

        for field_desc in self.added_fields:
            try:
                model_name, field_name = field_desc.split('.')
            except (TypeError, ValueError):
                raise ValueError('%r is not a valid field description.' % field_desc)

            model = models.get_model(self.migrations.app_label(), model_name)
            real_fields, meta, m2m_fields = self.split_model_def(model, model_defs[model_key(model)])
            yield ('AddField',
             {'model': model, 
                'field': model._meta.get_field_by_name(field_name)[0], 
                'field_def': real_fields[field_name]})

        for field_desc in self.added_indexes:
            try:
                model_name, field_name = field_desc.split('.')
            except (TypeError, ValueError):
                print('%r is not a valid field description.' % field_desc)

            model = models.get_model(self.migrations.app_label(), model_name)
            yield ('AddIndex',
             {'model': model, 
                'fields': [
                         model._meta.get_field_by_name(field_name)[0]]})


class InitialChanges(BaseChanges):
    """
    Creates all models; handles --initial.
    """

    def suggest_name(self):
        return 'initial'

    def __init__(self, migrations):
        self.migrations = migrations

    def get_changes(self):
        model_defs = freeze_apps([self.migrations.app_label()])
        for model in models.get_models(models.get_app(self.migrations.app_label())):
            if model._meta.abstract or getattr(model._meta, 'proxy', False) or not getattr(model._meta, 'managed', True):
                continue
            real_fields, meta, m2m_fields = self.split_model_def(model, model_defs[model_key(model)])
            yield (
             'AddModel',
             {'model': model, 
                'model_def': real_fields})
            if meta:
                for attr, operation in (('unique_together', 'AddUnique'), ('index_together', 'AddIndex')):
                    together = eval(meta.get(attr, '[]'))
                    if together:
                        if isinstance(together[0], string_types):
                            together = [
                             together]
                        for fields in together:
                            yield (
                             operation,
                             {'model': model, 
                                'fields': [ model._meta.get_field_by_name(x)[0] for x in fields ]})

            for name, triple in m2m_fields.items():
                field = model._meta.get_field_by_name(name)[0]
                if field.rel.through:
                    try:
                        through_model = field.rel.through_model
                    except AttributeError:
                        through_model = field.rel.through

                if not field.rel.through or getattr(through_model._meta, 'auto_created', False):
                    yield (
                     'AddM2M',
                     {'model': model, 
                        'field': field})