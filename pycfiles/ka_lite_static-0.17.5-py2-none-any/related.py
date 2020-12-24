# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/db/models/related.py
# Compiled at: 2018-07-11 18:15:30
from django.utils.encoding import smart_text
from django.db.models.fields import BLANK_CHOICE_DASH

class BoundRelatedObject(object):

    def __init__(self, related_object, field_mapping, original):
        self.relation = related_object
        self.field_mappings = field_mapping[related_object.name]

    def template_name(self):
        raise NotImplementedError

    def __repr__(self):
        return repr(self.__dict__)


class RelatedObject(object):

    def __init__(self, parent_model, model, field):
        self.parent_model = parent_model
        self.model = model
        self.opts = model._meta
        self.field = field
        self.name = '%s:%s' % (self.opts.app_label, self.opts.module_name)
        self.var_name = self.opts.object_name.lower()

    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH, limit_to_currently_related=False):
        """Returns choices with a default blank choices included, for use
        as SelectField choices for this field.

        Analogue of django.db.models.fields.Field.get_choices, provided
        initially for utilisation by RelatedFieldListFilter.
        """
        first_choice = include_blank and blank_choice or []
        queryset = self.model._default_manager.all()
        if limit_to_currently_related:
            queryset = queryset.complex_filter({'%s__isnull' % self.parent_model._meta.module_name: False})
        lst = [ (x._get_pk_val(), smart_text(x)) for x in queryset ]
        return first_choice + lst

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        return self.field.get_db_prep_lookup(lookup_type, value, connection=connection, prepared=prepared)

    def editable_fields(self):
        """Get the fields in this class that should be edited inline."""
        return [ f for f in self.opts.fields + self.opts.many_to_many if f.editable and f != self.field ]

    def __repr__(self):
        return '<RelatedObject: %s related to %s>' % (self.name, self.field.name)

    def bind(self, field_mapping, original, bound_related_object_class=BoundRelatedObject):
        return bound_related_object_class(self, field_mapping, original)

    def get_accessor_name(self):
        if self.field.rel.multiple:
            if getattr(self.field.rel, 'symmetrical', False) and self.model == self.parent_model:
                return
            return self.field.rel.related_name or self.opts.object_name.lower() + '_set'
        else:
            return self.field.rel.related_name or self.opts.object_name.lower()
            return

    def get_cache_name(self):
        return '_%s_cache' % self.get_accessor_name()