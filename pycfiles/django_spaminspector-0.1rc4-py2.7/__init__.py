# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/spaminspector/__init__.py
# Compiled at: 2011-07-22 10:22:56
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
if not hasattr(settings, 'SPAMINSPECTOR_AKISMET_KEY'):
    raise ImproperlyConfigured('You must define the SPAMINSPECTOR_AKISMET_KEY setting.')
settings.SPAMINSPECTOR_VIEWS = getattr(settings, 'SPAMINSPECTOR_VIEWS', (
 (
  'django.contrib.comments.views.comments.post_comment',
  {'comment_type': 'comment', 
     'comment_author': lambda request: request.POST.get('name', ''), 
     'comment_author_email': lambda request: request.POST.get('email', ''), 
     'comment_author_url': lambda request: request.POST.get('url', ''), 
     'comment_contents': lambda request: request.POST.get('comment', '')}),))
settings.SPAMINSPECTOR_SPAM_TEMPLATE = getattr(settings, 'SPAMINSPECTOR_SPAM_TEMPLATE', '')