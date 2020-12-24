# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-twitter-api/twitter_api/decorators.py
# Compiled at: 2015-11-01 17:29:06
from django.utils.functional import wraps
from django.db.models import Min

def opt_arguments(func):
    """
    Meta-decorator for ablity use decorators with optional arguments
    from here http://www.ellipsix.net/blog/2010/08/more-python-voodoo-optional-argument-decorators.html
    """

    def meta_wrapper(*args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            return func(args[0])
        else:

            def meta_func(inner_func):
                return func(inner_func, *args, **kwargs)

            return meta_func

    return meta_wrapper


@opt_arguments
def fetch_all(func, max_count):
    """
    Class method decorator for fetching all items. Add parameter `all=False` for decored method.
    If `all` is True, method runs as many times as it returns any results.
    Decorator receive 2 parameters:
      * integer `max_count` - max number of items method able to return
    Usage:

    @fetch_all(max_count=200)
    def fetch_something(self, ..., *kwargs):
        ....
    """

    def wrapper(self, all=False, return_instances=None, *args, **kwargs):
        if all:
            if return_instances is None:
                return_instances = []
            kwargs['count'] = max_count
            instances = func(self, *args, **kwargs)
            instances_count = len(instances)
            min_id = instances.aggregate(minid=Min('id'))['minid']
            return_instances += instances
            if instances_count > 1:
                kwargs['max_id'] = min_id
                return wrapper(self, all=True, return_instances=return_instances, *args, **kwargs)
            return self.model.objects.filter(id__in=[ instance.id for instance in return_instances ])
        else:
            return func(self, *args, **kwargs)
        return

    return wraps(func)(wrapper)