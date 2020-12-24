# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/variant/models.py
# Compiled at: 2014-08-25 20:18:47
from __future__ import unicode_literals
import random
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Experiment(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text=b"This is the name you'll use to reference this experiment in code and templates.")
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    variants = models.TextField(help_text=b"Provide a list of all variants you'd like to test, one variant name per line")

    def __str__(self):
        return self.name

    def get_variants(self):
        try:
            return self._variant_cache
        except AttributeError:
            self._variant_cache = [ v.strip() for v in self.variants.split(b'\n')
                                  ]

        return self._variant_cache

    def choose_variant(self):
        variants = self.get_variants()
        return random.choice(variants)