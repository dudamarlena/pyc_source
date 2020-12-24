# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yceruto/github/yceruto/django-ajax/django_ajax/encoder.py
# Compiled at: 2017-08-27 13:06:11
# Size of source mod 2**32: 1764 bytes
"""
Utils
"""
from __future__ import unicode_literals
import json
from django.http.response import HttpResponseRedirectBase, HttpResponse
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.db.models.base import ModelBase
from decimal import Decimal

class LazyJSONEncoderMixin(object):
    __doc__ = '\n    A JSONEncoder subclass that handle querysets and models objects.\n    Add how handle your type of object here to use when dump json\n\n    '

    def default(self, obj):
        if issubclass(type(obj), HttpResponseRedirectBase):
            return obj['Location']
        else:
            if issubclass(type(obj), TemplateResponse):
                return obj.rendered_content
            if issubclass(type(obj), HttpResponse):
                return obj.content
            if issubclass(type(obj), Exception) or isinstance(obj, bytes):
                pass
            return force_text(obj)
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        if isinstance(obj.__class__, ModelBase):
            return force_text(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        return super(LazyJSONEncoderMixin, self).default(obj)


class LazyJSONEncoder(LazyJSONEncoderMixin, json.JSONEncoder):
    pass


def serialize_to_json(data, *args, **kwargs):
    """
    A wrapper for simplejson.dumps with defaults as:

    cls=LazyJSONEncoder

    All arguments can be added via kwargs
    """
    kwargs['cls'] = kwargs.get('cls', LazyJSONEncoder)
    return json.dumps(data, *args, **kwargs)