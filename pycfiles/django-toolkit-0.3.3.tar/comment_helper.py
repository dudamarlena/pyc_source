# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/markup/comment_helper.py
# Compiled at: 2013-07-21 17:36:46


def get_object_comment_reference(instance, title=None):
    """
    Get an object reference for use within a comment so that it can be programatically
    referenced in the future (by a machine parsing the HTML...).
    """
    span = '<span data-object-type="%s.%s" data-object-pk="%s">%s</span>' % (
     instance.__module__,
     instance.__class__.__name__,
     instance.pk,
     instance if title is None else title)
    try:
        return '<a href="%s">%s</a>' % (
         instance.get_absolute_url(),
         span)
    except AttributeError:
        return span

    return