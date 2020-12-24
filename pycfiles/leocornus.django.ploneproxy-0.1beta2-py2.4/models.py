# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/django/ploneproxy/authen/models.py
# Compiled at: 2010-05-14 02:19:32
"""
models for Django Plone Proxy.
"""
from django.db.models import Model
from django.db.models import Manager
from django.db.models import IntegerField
from django.db.models import CharField
from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class PloneAuthenState(Model):
    """

    # trying the doctest
    >>> state = PloneAuthenState(user_id=1, status='valid',
    ... cookie_name='__ac', cookie_value='value')
    >>> state.save()

    # we should find it now.
    >>> theOne = PloneAuthenState.objects.get(user_id=1)
    >>> theOne.cookie_value
    u'value'
    """
    __module__ = __name__
    user_id = IntegerField(_('User Id'), primary_key=True)
    status = CharField(_('Authentication Status'), max_length=8)
    cookie_name = CharField(_('Cookie Name'), max_length=60)
    cookie_value = TextField(_('Cookie Value'))