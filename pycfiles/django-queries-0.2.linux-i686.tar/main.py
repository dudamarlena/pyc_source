# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/queries/views/main.py
# Compiled at: 2010-06-06 15:44:25
from queries.util import quote
from django.core.paginator import Paginator, InvalidPage
from django.db import models
from django.db.models.query import QuerySet
from django.utils.encoding import force_unicode, smart_str
from django.utils.translation import ugettext
from django.utils.http import urlencode
import operator
try:
    set
except NameError:
    from sets import Set as set

MAX_SHOW_ALL_ALLOWED = 200
ALL_VAR = 'all'
ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'
PAGE_VAR = 'p'
SEARCH_VAR = 'q'
TO_FIELD_VAR = 't'
IS_POPUP_VAR = 'pop'
ERROR_FLAG = 'e'
EMPTY_CHANGELIST_VALUE = '(None)'