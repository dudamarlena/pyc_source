# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/perms/object_perms.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 1047 bytes
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from tendenci.apps.perms.managers import ObjectPermissionManager
from tendenci.apps.user_groups.models import Group

class ObjectPermission(models.Model):
    __doc__ = "\n    Object level permissions\n\n    Don't move this model into the models.py\n    because it will cause circular references\n    all over the place. Please leave it here.\n    "
    user = models.ForeignKey(User, null=True, on_delete=(models.CASCADE))
    group = models.ForeignKey(Group, null=True, on_delete=(models.CASCADE))
    content_type = models.ForeignKey(ContentType, on_delete=(models.CASCADE))
    codename = models.CharField(max_length=255)
    object_id = models.IntegerField()
    create_dt = models.DateTimeField(auto_now_add=True)
    object = GenericForeignKey('content_type', 'object_id')
    objects = ObjectPermissionManager()

    class Meta:
        app_label = 'perms'