# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/models.py
# Compiled at: 2017-04-26 15:28:40
# Size of source mod 2**32: 583 bytes
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Testimonial(models.Model):
    content = models.TextField(_('Company Relationship'), max_length=3000)
    rating = models.FloatField(_('Rating'), validators=[MinValueValidator(0), MaxValueValidator(10)])
    user = models.ForeignKey('ovp_users.User', null=True, blank=True)
    published = models.BooleanField(_('Published'), default=False)
    created_date = models.DateTimeField(_('Created date'), auto_now_add=True)