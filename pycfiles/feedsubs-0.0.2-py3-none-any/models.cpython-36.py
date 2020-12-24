# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/models.py
# Compiled at: 2018-09-01 10:34:01
# Size of source mod 2**32: 581 bytes
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class UMProfile(models.Model):
    user = models.OneToOneField(User, on_delete=(models.CASCADE), related_name='um_profile')
    items_per_page = models.PositiveSmallIntegerField(default=20,
      validators=[
     MinValueValidator(1), MaxValueValidator(200)])
    deletion_pending = models.BooleanField(default=False)

    def __str__(self):
        return 'UMProfile of {}'.format(self.user)