# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/exceptions.py
# Compiled at: 2017-09-07 07:30:48
from django.utils.translation import ugettext as _

class MissingActionParam(Exception):

    def __init__(self, scope, param):
        Exception.__init__(self, _("'%s' param not provided for '%s'" % (
         param, scope)))