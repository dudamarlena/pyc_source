# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/decorators.py
# Compiled at: 2017-05-31 09:11:55
# Size of source mod 2**32: 802 bytes


def register(*models, **kwargs):
    """
    Registers the given model(s) classes into authorization object:

    @authorizations.register(Project)
    class ProjectAuthorization(options.BaseObjectAuthorization):
        pass
    """
    from .authorizations import Authorization, authorization

    def _authorization_wrapper(authorization_class):
        if not models:
            raise ValueError('At least one model must be passed to register.')
        authorization_obj = kwargs.pop('authorization', authorization)
        if not isinstance(authorization_obj, Authorization):
            raise ValueError('site must subclass Authorization')
        authorization_obj.register(models, authorization_class=authorization_class)
        return authorization_class

    return _authorization_wrapper