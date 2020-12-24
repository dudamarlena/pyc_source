# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/managers.py
# Compiled at: 2009-01-15 11:06:27
from django.db import models

class QuerySetManager(models.Manager):
    """
    A model manager using the model QuerySet.
    This allows chaining of extended filtering methods through the model manager,
    as described in http://simonwillison.net/2008/May/1/orm/

    Simply use an instance of this class as the (default) model manager, and
    add a QuerySet subclass (named ``QuerySet``) inside the model class defining
    all the methods that you need supported by the manager.
    
    For a detailed explanation, please see:

    http://simonwillison.net/2008/May/1/orm/
    """
    __module__ = __name__

    def get_query_set(self):
        return self.model.QuerySet(self.model)