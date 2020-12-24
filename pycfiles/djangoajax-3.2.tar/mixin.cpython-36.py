# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yceruto/github/yceruto/django-ajax/django_ajax/mixin.py
# Compiled at: 2017-08-27 12:59:16
# Size of source mod 2**32: 569 bytes
"""
Mixin Response
"""
from __future__ import unicode_literals
from django_ajax.decorators import ajax

class AJAXMixin(object):
    __doc__ = '\n    AJAX Mixin Class\n    '
    ajax_mandatory = True
    json_encoder = None

    def dispatch(self, request, *args, **kwargs):
        ajax_kwargs = {'mandatory': self.ajax_mandatory}
        if self.json_encoder:
            ajax_kwargs['cls'] = self.json_encoder
        return (ajax(**ajax_kwargs)(super(AJAXMixin, self).dispatch))(request, *args, **kwargs)