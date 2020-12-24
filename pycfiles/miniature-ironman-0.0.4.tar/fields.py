# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ir4y/projects/python/virtualenv/miniature_ve/miniature_ironman/miniature/models/fields.py
# Compiled at: 2014-04-11 02:07:18
from funcy import walk_values, compose
from django.db.models.fields import SlugField
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytils.translit import slugify
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^main\\.models\\.slug\\.AutoSlugField'])
except ImportError:
    pass

class AutoSlugField(SlugField):

    def __init__(self, *args, **kwargs):
        self.populate_from = kwargs.pop('populate_from', '')
        kwargs['blank'] = True
        kwargs['null'] = True
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)

        @receiver(post_save, sender=cls, weak=False)
        def setup_slug(sender, instance, **kwargs):
            data = walk_values(compose(slugify, unicode), instance.__dict__)
            slug = self.populate_from.format(**data)[:self.max_length]
            if slug != getattr(instance, name):
                setattr(instance, name, slug)
                instance.save()