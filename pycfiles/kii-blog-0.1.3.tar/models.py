# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/models.py
# Compiled at: 2015-01-07 11:09:36
from django.core.urlresolvers import reverse
import kii.stream.models, kii.base_models.fields

class Entry(kii.stream.models.StreamItem):
    slug = kii.base_models.fields.SlugField(populate_from=('title', ))