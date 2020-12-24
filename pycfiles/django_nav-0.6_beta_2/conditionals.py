# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\django_nav\conditionals.py
# Compiled at: 2010-05-05 10:07:53


def user_is_authenticated(context, *args, **kwargs):
    return context['user'].is_authenticated()


def user_is_staff(context, *args, **kwargs):
    return context['user'].is_staff


def user_has_perm(context, *args, **kwargs):
    perm = kwargs.pop('perm', args[0] if len(args) else None)
    return context['user'].has_perm(perm)