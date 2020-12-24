# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/boot/updates/contrib/admin/util.py
# Compiled at: 2016-05-20 23:26:49
from __future__ import unicode_literals
import datetime, decimal
from django.contrib.auth import get_permission_codename
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.db.models.deletion import Collector
from django.db.models.related import RelatedObject
from django.forms.forms import pretty_name
from django.utils import formats
from django.utils import six
from django.utils import timezone
from django.utils.encoding import force_str, force_text, smart_text
from django.utils.html import format_html
from django.utils.text import capfirst
from django.utils.translation import ungettext

def lookup_needs_distinct(opts, lookup_path):
    """
    Returns True if 'distinct()' should be used to query the given lookup path.
    """
    return False


def prepare_lookup_value(key, value):
    """
    Returns a lookup value prepared to be used in queryset filtering.
    """
    if key.endswith(b'__in'):
        value = value.split(b',')
    if key.endswith(b'__isnull'):
        if value.lower() in ('', 'false', '0'):
            value = False
        else:
            value = True
    return value


def quote(s):
    """
    Ensure that primary key values do not confuse the admin URLs by escaping
    any '/', '_' and ':' and similarly problematic characters.
    Similar to urllib.quote, except that the quoting is slightly different so
    that it doesn't get automatically unquoted by the Web browser.
    """
    if not isinstance(s, six.string_types):
        return s
    res = list(s)
    for i in xrange(len(res)):
        c = res[i]
        if c in b':/_#?;@&=+$,"<>%\\':
            res[i] = b'_%02X' % ord(c)

    return (b'').join(res)


def unquote(s):
    """
    Undo the effects of quote(). Based heavily on urllib.unquote().
    """
    mychr = chr
    myatoi = int
    list = s.split(b'_')
    res = [list[0]]
    myappend = res.append
    del list[0]
    for item in list:
        if item[1:2]:
            try:
                myappend(mychr(myatoi(item[:2], 16)) + item[2:])
            except ValueError:
                myappend(b'_' + item)

        else:
            myappend(b'_' + item)

    return (b'').join(res)


def flatten_fieldsets(fieldsets):
    """Returns a list of field names from an admin fieldsets structure."""
    field_names = []
    for name, opts in fieldsets:
        for field in opts[b'fields']:
            if isinstance(field, (list, tuple)):
                field_names.extend(field)
            else:
                field_names.append(field)

    return field_names


def get_deleted_objects(objs, opts, user, admin_site, using):
    """
    Find all objects related to ``objs`` that should also be deleted. ``objs``
    must be a homogenous iterable of objects (e.g. a QuerySet).

    Returns a nested list of strings suitable for display in the
    template with the ``unordered_list`` filter.

    """
    collector = NestedObjects(using=using)
    collector.collect(objs)
    perms_needed = set()

    def format_callback(obj):
        has_admin = obj.__class__ in admin_site._registry
        opts = obj._meta
        if has_admin:
            admin_url = reverse(b'%s:%s_%s_change' % (
             admin_site.name,
             opts.app_label,
             opts.model_name), None, (quote(obj._get_pk_val()),))
            p = b'%s.%s' % (opts.app_label,
             get_permission_codename(b'delete', opts))
            if not user.has_perm(p):
                perms_needed.add(opts.verbose_name)
            return format_html(b'{0}: <a href="{1}">{2}</a>', capfirst(opts.verbose_name), admin_url, obj)
        else:
            return b'%s: %s' % (capfirst(opts.verbose_name),
             force_text(obj))
            return

    to_delete = collector.nested(format_callback)
    protected = [ format_callback(obj) for obj in collector.protected ]
    return (
     to_delete, perms_needed, protected)


class NestedObjects(Collector):

    def __init__(self, *args, **kwargs):
        super(NestedObjects, self).__init__(*args, **kwargs)
        self.edges = {}
        self.protected = set()

    def add_edge(self, source, target):
        self.edges.setdefault(source, []).append(target)

    def collect(self, objs, source_attr=None, **kwargs):
        for obj in objs:
            if source_attr:
                self.add_edge(getattr(obj, source_attr), obj)
            else:
                self.add_edge(None, obj)

        try:
            return super(NestedObjects, self).collect(objs, source_attr=source_attr, **kwargs)
        except models.ProtectedError as e:
            self.protected.update(e.protected_objects)

        return

    def related_objects(self, related, objs):
        qs = super(NestedObjects, self).related_objects(related, objs)
        return qs.select_related(related.field.name)

    def _nested(self, obj, seen, format_callback):
        if obj in seen:
            return []
        seen.add(obj)
        children = []
        for child in self.edges.get(obj, ()):
            children.extend(self._nested(child, seen, format_callback))

        if format_callback:
            ret = [
             format_callback(obj)]
        else:
            ret = [
             obj]
        if children:
            ret.append(children)
        return ret

    def nested(self, format_callback=None):
        """
        Return the graph as a nested list.

        """
        seen = set()
        roots = []
        for root in self.edges.get(None, ()):
            roots.extend(self._nested(root, seen, format_callback))

        return roots

    def can_fast_delete(self, *args, **kwargs):
        """
        We always want to load the objects into memory so that we can display
        them to the user in confirm page.
        """
        return False


def model_format_dict(obj):
    """
    Return a `dict` with keys 'verbose_name' and 'verbose_name_plural',
    typically for use with string formatting.

    `obj` may be a `Model` instance, `Model` subclass, or `QuerySet` instance.

    """
    if isinstance(obj, (models.Model, models.base.ModelBase)):
        opts = obj._meta
    elif isinstance(obj, models.query.QuerySet):
        opts = obj.model._meta
    else:
        opts = obj
    return {b'verbose_name': force_text(opts.verbose_name), b'verbose_name_plural': force_text(opts.verbose_name_plural)}


def model_ngettext(obj, n=None):
    """
    Return the appropriate `verbose_name` or `verbose_name_plural` value for
    `obj` depending on the count `n`.

    `obj` may be a `Model` instance, `Model` subclass, or `QuerySet` instance.
    If `obj` is a `QuerySet` instance, `n` is optional and the length of the
    `QuerySet` is used.

    """
    if isinstance(obj, models.query.QuerySet):
        if n is None:
            n = obj.count()
        obj = obj.model
    d = model_format_dict(obj)
    singular, plural = d[b'verbose_name'], d[b'verbose_name_plural']
    return ungettext(singular, plural, n or 0)


def lookup_field(name, obj, model_admin=None):
    opts = obj._meta
    try:
        f = opts.get_field(name)
    except models.FieldDoesNotExist:
        if callable(name):
            attr = name
            value = attr(obj)
        elif model_admin is not None and hasattr(model_admin, name) and not name == b'__str__' and not name == b'__unicode__':
            attr = getattr(model_admin, name)
            value = attr(obj)
        else:
            attr = getattr(obj, name)
            if callable(attr):
                value = attr()
            else:
                value = attr
        f = None
    else:
        attr = None
        value = getattr(obj, name)

    return (
     f, attr, value)


def label_for_field(name, model, model_admin=None, return_attr=False):
    """
    Returns a sensible label for a field name. The name can be a callable,
    property (but not created with @property decorator) or the name of an
    object's attribute, as well as a genuine fields. If return_attr is
    True, the resolved attribute (which could be a callable) is also returned.
    This will be None if (and only if) the name refers to a field.
    """
    attr = None
    try:
        field = model._meta.get_field_by_name(name)[0]
        if isinstance(field, RelatedObject):
            label = field.opts.verbose_name
        else:
            label = field.verbose_name
    except models.FieldDoesNotExist:
        if name == b'__unicode__':
            label = force_text(model._meta.verbose_name)
            attr = six.text_type
        elif name == b'__str__':
            label = force_str(model._meta.verbose_name)
            attr = bytes
        else:
            if callable(name):
                attr = name
            elif model_admin is not None and hasattr(model_admin, name):
                attr = getattr(model_admin, name)
            elif hasattr(model, name):
                attr = getattr(model, name)
            else:
                message = b"Unable to lookup '%s' on %s" % (name, model._meta.object_name)
                if model_admin:
                    message += b' or %s' % (model_admin.__class__.__name__,)
                raise AttributeError(message)
            if hasattr(attr, b'short_description'):
                label = attr.short_description
            elif isinstance(attr, property) and hasattr(attr, b'fget') and hasattr(attr.fget, b'short_description'):
                label = attr.fget.short_description
            elif callable(attr):
                if attr.__name__ == b'<lambda>':
                    label = b'--'
                else:
                    label = pretty_name(attr.__name__)
            else:
                label = pretty_name(name)

    if return_attr:
        return (label, attr)
    else:
        return label
        return


def help_text_for_field(name, model):
    help_text = b''
    try:
        field_data = model._meta.get_field_by_name(name)
    except models.FieldDoesNotExist:
        pass

    field = field_data[0]
    if not isinstance(field, RelatedObject):
        help_text = field.help_text
    return smart_text(help_text)


def display_for_field(value, field):
    from django.contrib.admin.templatetags.admin_list import _boolean_icon
    from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
    if field.flatchoices:
        return dict(field.flatchoices).get(value, EMPTY_CHANGELIST_VALUE)
    else:
        if isinstance(field, models.BooleanField) or isinstance(field, models.NullBooleanField):
            return _boolean_icon(value)
        else:
            if value is None:
                return EMPTY_CHANGELIST_VALUE
            if isinstance(field, models.DateTimeField):
                return formats.localize(timezone.template_localtime(value))
            if isinstance(field, (models.DateField, models.TimeField)):
                return formats.localize(value)
            if isinstance(field, models.DecimalField):
                return formats.number_format(value, field.decimal_places)
            if isinstance(field, models.FloatField):
                return formats.number_format(value)
            return smart_text(value)

        return


def display_for_value(value, boolean=False):
    from django.contrib.admin.templatetags.admin_list import _boolean_icon
    from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
    if boolean:
        return _boolean_icon(value)
    else:
        if value is None:
            return EMPTY_CHANGELIST_VALUE
        else:
            if isinstance(value, datetime.datetime):
                return formats.localize(timezone.template_localtime(value))
            if isinstance(value, (datetime.date, datetime.time)):
                return formats.localize(value)
            if isinstance(value, six.integer_types + (decimal.Decimal, float)):
                return formats.number_format(value)
            return smart_text(value)

        return


class NotRelationField(Exception):
    pass


def get_model_from_relation(field):
    if hasattr(field, b'get_path_info'):
        return field.get_path_info()[(-1)].to_opts.model
    if isinstance(field, models.related.RelatedObject):
        return field.model
    if getattr(field, b'rel'):
        return field.rel.to
    raise NotRelationField


def reverse_field_path(model, path):
    """ Create a reversed field path.

    E.g. Given (Order, "user__groups"),
    return (Group, "user__order").

    Final field must be a related model, not a data field.

    """
    reversed_path = []
    parent = model
    pieces = path.split(LOOKUP_SEP)
    for piece in pieces:
        field, model, direct, m2m = parent._meta.get_field_by_name(piece)
        if len(reversed_path) == len(pieces) - 1:
            try:
                get_model_from_relation(field)
            except NotRelationField:
                break

        if direct:
            related_name = field.related_query_name()
            parent = field.rel.to
        else:
            related_name = field.field.name
            parent = field.model
        reversed_path.insert(0, related_name)

    return (
     parent, LOOKUP_SEP.join(reversed_path))


def get_fields_from_path(model, path):
    """ Return list of Fields given path relative to model.

    e.g. (ModelX, "user__groups__name") -> [
        <django.db.models.fields.related.ForeignKey object at 0x...>,
        <django.db.models.fields.related.ManyToManyField object at 0x...>,
        <django.db.models.fields.CharField object at 0x...>,
    ]
    """
    pieces = path.split(LOOKUP_SEP)
    fields = []
    for piece in pieces:
        if fields:
            parent = get_model_from_relation(fields[(-1)])
        else:
            parent = model
        fields.append(parent._meta.get_field_by_name(piece)[0])

    return fields


def remove_trailing_data_field(fields):
    """ Discard trailing non-relation field if extant. """
    try:
        get_model_from_relation(fields[(-1)])
    except NotRelationField:
        fields = fields[:-1]

    return fields


def get_limit_choices_to_from_path(model, path):
    """ Return Q object for limiting choices if applicable.

    If final model in path is linked via a ForeignKey or ManyToManyField which
    has a `limit_choices_to` attribute, return it as a Q object.
    """
    fields = get_fields_from_path(model, path)
    fields = remove_trailing_data_field(fields)
    limit_choices_to = fields and hasattr(fields[(-1)], b'rel') and getattr(fields[(-1)].rel, b'limit_choices_to', None)
    if not limit_choices_to:
        return models.Q()
    else:
        if isinstance(limit_choices_to, models.Q):
            return limit_choices_to
        else:
            return models.Q(**limit_choices_to)

        return