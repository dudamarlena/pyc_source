# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/queries/models.py
# Compiled at: 2010-05-09 07:06:47
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from queries.util import quote
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe
ADDITION = 1
CHANGE = 2
DELETION = 3