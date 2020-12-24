# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_html_comments/models.py
# Compiled at: 2016-11-21 18:03:27
from mezzanine.generic.models import ThreadedComment
from sanitize import sanitize
from django_comments.signals import comment_was_posted
from django.utils.module_loading import import_string
from django.conf import settings
comment_class = import_string(settings.COMMENT_CLASS)

def comment_sanitizer(sender, comment, request, **kwargs):
    comment.comment = sanitize(comment.comment)
    comment.save()


def comment_filter(comment_text):
    return comment_text


comment_was_posted.connect(comment_sanitizer, sender=ThreadedComment)