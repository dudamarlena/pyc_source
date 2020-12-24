# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/order/utils.py
# Compiled at: 2011-09-15 05:06:32
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import get_model
from django.db.models.query import QuerySet
try:
    from django.utils.decorators import method_decorator
except ImportError:
    method_decorator = lambda x: x

try:
    from django.views.decorators.csrf import csrf_protect
except ImportError:
    csrf_protect = lambda x: x

csrf_protect_m = method_decorator(csrf_protect)

def create_order_classes(model_label, order_field_names):
    """
    Create order model and admin class.
    Add order model to order.models module and register admin class.
    Connect ordered_objects manager to related model.
    """
    labels = resolve_labels(model_label)
    model = get_model(labels['app'], labels['model'])

    class OrderItemBase(models.Model):
        """
        Dynamic order class base.
        """
        item = models.ForeignKey(model_label)
        timestamp = models.DateTimeField(auto_now=True)

        class Meta:
            abstract = True
            app_label = 'order'

    class Admin(admin.ModelAdmin):
        """
        Dynamic order admin class.
        """
        list_display = ('item_link', ) + tuple(order_field_names)
        list_editable = order_field_names

        def get_model_perms(self, request):
            """
            Return empty perms dict thus hiding the model from admin index.
            """
            return {}

        @csrf_protect_m
        def changelist_view(self, request, extra_context=None):
            list_url = reverse('admin:%s_%s_changelist' % (labels['app'],
             labels['model'].lower()))
            add_url = reverse('admin:%s_%s_add' % (labels['app'],
             labels['model'].lower()))
            result = super(Admin, self).changelist_view(request, extra_context={'add_url': add_url, 
               'list_url': list_url, 
               'related_opts': model._meta})
            return result

        def item_link(self, obj):
            url = reverse('admin:%s_%s_change' % (labels['app'],
             labels['model'].lower()), args=(obj.item.id,))
            return '<a href="%s">%s</a>' % (url, str(obj.item))

        item_link.allow_tags = True
        item_link.short_description = 'Item'

    attrs = {'__module__': 'order.models'}
    fields = {}
    for field in order_field_names:
        fields[field] = models.IntegerField()

    attrs.update(fields)
    order_item_class_name = resolve_order_item_class_name(labels)
    order_model = type(order_item_class_name, (OrderItemBase,), attrs)
    admin.site.register(order_model, Admin)
    from order import managers
    setattr(QuerySet, 'user_order_by', managers.user_order_by)
    return order_model


def create_order_objects(model, order_fields):
    """
    Create order items for objects already present in the database.
    """
    for rel in model._meta.get_all_related_objects():
        rel_model = rel.model
        if rel_model.__module__ == 'order.models':
            objs = model.objects.all()
            values = {}
            for order_field in order_fields:
                order_objs = rel_model.objects.all().order_by('-%s' % order_field)
                try:
                    values[order_field] = getattr(order_objs[0], order_field) + 1
                except IndexError:
                    values[order_field] = 1

            for obj in objs:
                try:
                    rel_model.objects.get(item=obj)
                except rel_model.DoesNotExist:
                    rel_model.objects.create(item=obj, **values)
                    for key in values:
                        values[key] += 1


def is_orderable(cls):
    """
    Checks if the provided class is specified as an orderable in
    settings.ORDERABLE_MODELS. If it is return its settings.
    """
    if not getattr(settings, 'ORDERABLE_MODELS', None):
        return False
    else:
        labels = resolve_labels(cls)
        if labels['app_model'] in settings.ORDERABLE_MODELS:
            return settings.ORDERABLE_MODELS[labels['app_model']]
        return False


def resolve_labels(model_label):
    """
    Seperate model_label into parts.
    Returns dictionary with app, model and app_model strings.
    """
    labels = {}
    labels['app'] = model_label.split('.')[0]
    labels['model'] = model_label.split('.')[(-1)]
    labels['app_model'] = '%s.%s' % (labels['app'], labels['model'])
    return labels


def resolve_order_item_class_name(labels):
    """
    Returns an OrderItem class name for provided class.
    """
    return '%sOrderItem' % labels['model']


def resolve_order_item_related_set_name(labels):
    """
    Returns a reverse relation manager name to order items for class.
    """
    return ('%sorderitem_set' % labels['model']).lower()


def sanitize_order(model):
    """
    Sanitize order values so eliminate conflicts and gaps.
    XXX: Early start, very ugly, needs work.
    """
    to_order_dict = {}
    order_field_names = []
    for field in model._meta.fields:
        if isinstance(field, models.IntegerField):
            order_field_names.append(field.name)

    for field_name in order_field_names:
        to_order_dict[field_name] = list(model.objects.all().order_by(field_name, '-timestamp'))

    updates = {}
    for (field_name, object_list) in to_order_dict.items():
        for (i, obj) in enumerate(object_list):
            position = i + 1
            if getattr(obj, field_name) != position:
                if obj in updates:
                    updates[obj][field_name] = position
                else:
                    updates[obj] = {field_name: position}

    for (obj, fields) in updates.items():
        for (field, value) in fields.items():
            setattr(obj, field, value)

        obj.save()