# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/fields/reverse_related.py
# Compiled at: 2019-02-14 00:35:17
"""
"Rel objects" for related fields.

"Rel objects" (for lack of a better name) carry information about the relation
modeled by a related field and provide some utility functions. They're stored
in the ``remote_field`` attribute of the field.

They also act as reverse fields for the purposes of the Meta API because
they're the closest concept currently available.
"""
from __future__ import unicode_literals
import warnings
from django.core import exceptions
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from . import BLANK_CHOICE_DASH

class ForeignObjectRel(object):
    """
    Used by ForeignObject to store information about the relation.

    ``_meta.get_fields()`` returns this class to provide access to the field
    flags for the reverse relation.
    """
    auto_created = True
    concrete = False
    editable = False
    is_relation = True
    null = True

    def __init__(self, field, to, related_name=None, related_query_name=None, limit_choices_to=None, parent_link=False, on_delete=None):
        self.field = field
        self.model = to
        self.related_name = related_name
        self.related_query_name = related_query_name
        self.limit_choices_to = {} if limit_choices_to is None else limit_choices_to
        self.parent_link = parent_link
        self.on_delete = on_delete
        self.symmetrical = False
        self.multiple = True
        return

    @property
    def to(self):
        warnings.warn(b'Usage of ForeignObjectRel.to attribute has been deprecated. Use the model attribute instead.', RemovedInDjango20Warning, 2)
        return self.model

    @cached_property
    def hidden(self):
        return self.is_hidden()

    @cached_property
    def name(self):
        return self.field.related_query_name()

    @property
    def remote_field(self):
        return self.field

    @property
    def target_field(self):
        """
        When filtering against this relation, returns the field on the remote
        model against which the filtering should happen.
        """
        target_fields = self.get_path_info()[(-1)].target_fields
        if len(target_fields) > 1:
            raise exceptions.FieldError(b"Can't use target_field for multicolumn relations.")
        return target_fields[0]

    @cached_property
    def related_model(self):
        if not self.field.model:
            raise AttributeError(b"This property can't be accessed before self.field.contribute_to_class has been called.")
        return self.field.model

    @cached_property
    def many_to_many(self):
        return self.field.many_to_many

    @cached_property
    def many_to_one(self):
        return self.field.one_to_many

    @cached_property
    def one_to_many(self):
        return self.field.many_to_one

    @cached_property
    def one_to_one(self):
        return self.field.one_to_one

    def get_lookup(self, lookup_name):
        return self.field.get_lookup(lookup_name)

    def get_internal_type(self):
        return self.field.get_internal_type()

    @property
    def db_type(self):
        return self.field.db_type

    def __repr__(self):
        return b'<%s: %s.%s>' % (
         type(self).__name__,
         self.related_model._meta.app_label,
         self.related_model._meta.model_name)

    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH):
        """
        Return choices with a default blank choices included, for use as
        SelectField choices for this field.

        Analog of django.db.models.fields.Field.get_choices(), provided
        initially for utilization by RelatedFieldListFilter.
        """
        return (blank_choice if include_blank else []) + [ (x._get_pk_val(), force_text(x)) for x in self.related_model._default_manager.all() ]

    def is_hidden(self):
        """Should the related object be hidden?"""
        return bool(self.related_name) and self.related_name[(-1)] == b'+'

    def get_joining_columns(self):
        return self.field.get_reverse_joining_columns()

    def get_extra_restriction(self, where_class, alias, related_alias):
        return self.field.get_extra_restriction(where_class, related_alias, alias)

    def set_field_name(self):
        """
        Set the related field's name, this is not available until later stages
        of app loading, so set_field_name is called from
        set_attributes_from_rel()
        """
        self.field_name = None
        return

    def get_accessor_name(self, model=None):
        opts = model._meta if model else self.related_model._meta
        model = model or self.related_model
        if self.multiple:
            if self.symmetrical and model == self.model:
                return None
        if self.related_name:
            return self.related_name
        else:
            return opts.model_name + (b'_set' if self.multiple else b'')

    def get_cache_name(self):
        return b'_%s_cache' % self.get_accessor_name()

    def get_path_info(self):
        return self.field.get_reverse_path_info()


class ManyToOneRel(ForeignObjectRel):
    """
    Used by the ForeignKey field to store information about the relation.

    ``_meta.get_fields()`` returns this class to provide access to the field
    flags for the reverse relation.

    Note: Because we somewhat abuse the Rel objects by using them as reverse
    fields we get the funny situation where
    ``ManyToOneRel.many_to_one == False`` and
    ``ManyToOneRel.one_to_many == True``. This is unfortunate but the actual
    ManyToOneRel class is a private API and there is work underway to turn
    reverse relations into actual fields.
    """

    def __init__(self, field, to, field_name, related_name=None, related_query_name=None, limit_choices_to=None, parent_link=False, on_delete=None):
        super(ManyToOneRel, self).__init__(field, to, related_name=related_name, related_query_name=related_query_name, limit_choices_to=limit_choices_to, parent_link=parent_link, on_delete=on_delete)
        self.field_name = field_name

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop(b'related_model', None)
        return state

    def get_related_field(self):
        """
        Return the Field in the 'to' object to which this relationship is tied.
        """
        field = self.model._meta.get_field(self.field_name)
        if not field.concrete:
            raise exceptions.FieldDoesNotExist(b"No related field named '%s'" % self.field_name)
        return field

    def set_field_name(self):
        self.field_name = self.field_name or self.model._meta.pk.name


class OneToOneRel(ManyToOneRel):
    """
    Used by OneToOneField to store information about the relation.

    ``_meta.get_fields()`` returns this class to provide access to the field
    flags for the reverse relation.
    """

    def __init__(self, field, to, field_name, related_name=None, related_query_name=None, limit_choices_to=None, parent_link=False, on_delete=None):
        super(OneToOneRel, self).__init__(field, to, field_name, related_name=related_name, related_query_name=related_query_name, limit_choices_to=limit_choices_to, parent_link=parent_link, on_delete=on_delete)
        self.multiple = False


class ManyToManyRel(ForeignObjectRel):
    """
    Used by ManyToManyField to store information about the relation.

    ``_meta.get_fields()`` returns this class to provide access to the field
    flags for the reverse relation.
    """

    def __init__(self, field, to, related_name=None, related_query_name=None, limit_choices_to=None, symmetrical=True, through=None, through_fields=None, db_constraint=True):
        super(ManyToManyRel, self).__init__(field, to, related_name=related_name, related_query_name=related_query_name, limit_choices_to=limit_choices_to)
        if through and not db_constraint:
            raise ValueError(b"Can't supply a through model and db_constraint=False")
        self.through = through
        if through_fields and not through:
            raise ValueError(b'Cannot specify through_fields without a through model')
        self.through_fields = through_fields
        self.symmetrical = symmetrical
        self.db_constraint = db_constraint

    def get_related_field(self):
        """
        Return the field in the 'to' object to which this relationship is tied.
        Provided for symmetry with ManyToOneRel.
        """
        opts = self.through._meta
        if self.through_fields:
            field = opts.get_field(self.through_fields[0])
        else:
            for field in opts.fields:
                rel = getattr(field, b'remote_field', None)
                if rel and rel.model == self.model:
                    break

        return field.foreign_related_fields[0]