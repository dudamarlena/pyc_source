# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forums/compat.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 2135 bytes
from django.conf import settings
from django.utils.encoding import force_text
from unidecode import unidecode

def get_image_field_class():
    try:
        from sorl.thumbnail import ImageField
    except ImportError:
        from django.db.models import ImageField

    return ImageField


def get_image_field_full_name():
    try:
        from sorl.thumbnail import ImageField
        name = 'sorl.thumbnail.fields.ImageField'
    except ImportError:
        from django.db.models import ImageField
        name = 'django.db.models.fields.files.ImageField'

    return name


def get_user_model():
    from django.contrib.auth import get_user_model
    return get_user_model()


def get_user_model_path():
    return getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def get_username_field():
    return get_user_model().USERNAME_FIELD


def get_atomic_func():
    try:
        import django.db.transaction as atomic_func
    except ImportError:
        import django.db.transaction as atomic_func

    return atomic_func


def get_paginator_class():
    try:
        from pure_pagination import Paginator
        pure_pagination = True
    except ImportError:
        from django.core.paginator import Paginator, Page

        class PageRepr(int):

            def querystring(self):
                return 'page=%s' % self

        Page.pages = lambda self: [PageRepr(i) for i in range(1, self.paginator.num_pages + 1)]
        pure_pagination = False

    return (Paginator, pure_pagination)


def is_installed(app_name):
    import django.apps as apps
    return apps.is_installed(app_name)


def get_related_model_class(parent_model, field_name):
    return parent_model._meta.get_field(field_name).related_model


def slugify(text):
    """
    Slugify function that supports unicode symbols
    :param text: any unicode text
    :return: slugified version of passed text
    """
    import django.utils.text as django_slugify
    return django_slugify(force_text(unidecode(text)))