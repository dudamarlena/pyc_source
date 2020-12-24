# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/docs/diagrams.py
# Compiled at: 2019-04-02 21:14:52
# Size of source mod 2**32: 3768 bytes
import json
from django.conf import settings
from djangoplus.cache import CACHE
from django.utils import translation
import django.utils.translation as _
from djangoplus.utils.metadata import get_metadata

class Workflow(object):

    def __init__(self):
        translation.activate(settings.LANGUAGE_CODE)
        self.actors = []
        self.tasks = []
        tmp = None
        for task in CACHE['WORKFLOWS']:
            role = task['role']
            activity = task['activity']
            model = task['model']
            if role != tmp:
                tmp = role or _('Superuser')
                action = _('Acessar como')
                self.tasks.append('{} {}'.format(action, tmp))
            elif model:
                action = '{}{}{}'.format(activity, _(' in '), model)
            else:
                action = activity
            self.tasks.append(action)


class ClassDiagram(object):
    POSITION_MAP = {1:(2.2, ), 
     2:(1.2, 3.2),  3:(3.2, 1.1, 1.3),  4:(2.2, 3.2, 1.1, 1.3),  5:(2.2, 1.1, 1.3, 3.1, 3.3),  6:(1.2, 3.2, 1.1, 3.1, 1.3, 3.3), 
     7:(2.2, 1.2, 3.2, 1.1, 1.3, 3.1, 3.3),  8:(1.2, 3.2, 1.1, 1.3, 2.1, 2.3, 3.1, 3.3), 
     9:(1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3)}

    def __init__(self, class_diagram_name, models):
        self.name = class_diagram_name
        self.classes = []
        self.compositions = []
        self.agregations = []
        classes = dict()
        n = len(CACHE['CLASS_DIAGRAMS'][class_diagram_name])
        associations_count = {}
        for model in CACHE['CLASS_DIAGRAMS'][class_diagram_name]:
            associations_count[model] = 0

        for model in CACHE['CLASS_DIAGRAMS'][class_diagram_name]:
            verbose_name = get_metadata(model, 'verbose_name')
            related_objects = get_metadata(model, 'related_objects')
            classes[model] = dict(name=verbose_name, position='1.1')
            for related_object in related_objects:
                related_verbose_name = get_metadata(related_object.related_model, 'verbose_name')
                if related_object.related_model in models:
                    if hasattr(related_object.field, 'composition'):
                        if related_object.field.composition:
                            self.compositions.append([
                             related_verbose_name, verbose_name, related_object.remote_field.name])
                            associations_count[model] += 1
                            associations_count[related_object.related_model] += 1
                    first_condition = model not in CACHE['ROLE_MODELS'] or class_diagram_name == related_verbose_name
                    second_condition = class_diagram_name == verbose_name and related_object.related_model not in CACHE['ROLE_MODELS']
                    if first_condition or second_condition:
                        self.agregations.append([
                         verbose_name, related_verbose_name, related_object.field.name])
                        associations_count[related_object.related_model] += 1
                        associations_count[model] += 1

        sorted_associations_count = sorted(associations_count, key=(associations_count.get), reverse=True)
        for i, model in enumerate(sorted_associations_count):
            cls = classes[model]
            cls['position'] = ClassDiagram.POSITION_MAP[n][i]
            self.classes.append(cls)

    def as_dict(self):
        return dict(name=(self.name), classes=(self.classes), compositions=(self.compositions), agregations=(self.agregations))

    def as_json(self):
        return json.dumps(self.as_dict())