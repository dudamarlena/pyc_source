# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/mixins.py
# Compiled at: 2017-03-15 11:34:46
# Size of source mod 2**32: 1868 bytes
from jsonattrs.models import Schema
from collections import defaultdict
import itertools

def template_xlang_labels(attr):
    try:
        labels = ['data-label-{}="{}"'.format(k, v) for k, v in sorted(attr.items())]
        return ' '.join(labels)
    except AttributeError:
        return ''


def xlang_choices(attr, value):
    if attr.choices:
        try:
            xlang_c = dict(zip(attr.choices, attr.choice_labels_xlat))
            if isinstance(value, (tuple, list)):
                try:
                    labels = [xlang_c[k].items() for k in xlang_c if k in value]
                    xlang_labels = defaultdict(list)
                    for k, v in list(itertools.chain(*labels)):
                        xlang_labels[k].append(v)

                    xlang_labels = {k:', '.join(sorted(v)) for k, v in xlang_labels.items()}
                    return template_xlang_labels(xlang_labels)
                except AttributeError:
                    pass

            return template_xlang_labels(xlang_c.get(value))
        except TypeError:
            pass

        return ''


class JsonAttrsMixin:

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = self.object
        field = self.attributes_field
        obj_attrs = getattr(obj, field)
        schemas = Schema.objects.from_instance(obj)
        attrs = [a for s in schemas for a in s.attributes.all()]
        context[field] = [(a.long_name, a.render(obj_attrs.get(a.name, '—')), template_xlang_labels(a.long_name_xlat), xlang_choices(a, obj_attrs.get(a.name, '—'))) for a in attrs if not a.omit]
        return context