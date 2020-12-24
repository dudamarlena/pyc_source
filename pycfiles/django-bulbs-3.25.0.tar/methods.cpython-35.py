# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/utils/methods.py
# Compiled at: 2016-09-28 11:20:42
# Size of source mod 2**32: 4055 bytes
from datetime import date, datetime
from dateutil import tz
from importlib import import_module
from six import string_types, text_type, binary_type
from six.moves.urllib.parse import urlencode
from django import template
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.apps import apps
from django.shortcuts import get_object_or_404
INVALID_TEMPLATE_CHOICE = 'Choices for template values must be non-zero integers.'

def get_central_now():
    utc_now = timezone.now()
    central_tz = tz.gettz('America/Chicago')
    central_now = utc_now.astimezone(central_tz)
    return central_now


def today():
    return getattr(settings, 'TODAY', get_central_now())


def today_as_utc_datetime():
    """Datetime/Date comparisons aren't great, and someone might configure TODAY, to be a date."""
    now = today()
    if not isinstance(now, datetime) and isinstance(now, date):
        now = datetime.combine(now, datetime.min.time())
        now = now.replace(tzinfo=tz.gettz('UTC'))
    return now


def get_query_params(request):
    try:
        return request.query_params
    except:
        return request.QUERY_PARAMS


def get_request_data(request):
    try:
        return request.data
    except:
        return request.DATA


def is_str(value):
    return isinstance(value, (string_types, text_type, binary_type))


def is_valid_digit(value):
    if isinstance(value, (int, float)):
        return True
    if is_str(value):
        return value.isdigit()
    return False


def datetime_to_epoch_seconds(value):
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    return (value - epoch).total_seconds()


def get_template_choices():
    configured_templates = getattr(settings, 'BULBS_TEMPLATE_CHOICES', ())
    for choice in configured_templates:
        if choice[0] == 0:
            raise ValueError(INVALID_TEMPLATE_CHOICE.format(choice))
        elif type(choice[0]) != int:
            raise ValueError(INVALID_TEMPLATE_CHOICE.format(choice))

    return ((0, None), ) + configured_templates


def get_overridable_template_name(parent_name, child_name, must_inherit=True):
    get_template = template.loader.get_template
    try:
        child_template = get_template(child_name)
    except template.loader.TemplateDoesNotExist:
        child_template = None

    if child_template and must_inherit:
        bad_inheritance_message = '{} MUST extend {}'.format(child_name, parent_name)
        extends_node = child_template.template.nodelist.get_nodes_by_type(template.loader_tags.ExtendsNode)
        if not extends_node[0]:
            raise Exception(bad_inheritance_message)
        if str(extends_node[0].parent_name) != "'{}'".format(parent_name):
            raise Exception(bad_inheritance_message)
        if child_template:
            template_name = child_name
    else:
        template_name = parent_name
    return template_name


def get_video_object_from_videohub_id(videohub_id):
    video_model = apps.get_model(settings.VIDEO_MODEL)
    return get_object_or_404(video_model, videohub_ref_id=int(videohub_id))


def redirect_unpublished_to_login_or_404(request, next_url, next_params=None):
    redirect_unpublished = getattr(settings, 'REDIRECT_UNPUBLISHED_TO_LOGIN', True)
    if not request.user.is_authenticated() and redirect_unpublished:
        if next_params:
            next_url += '?' + urlencode(next_params)
        return HttpResponseRedirect('{}?{}'.format(settings.LOGIN_URL, urlencode({'next': next_url})))
    raise Http404


def import_class(name):
    """Load class from fully-qualified python module name.

    ex: import_class('bulbs.content.models.Content')
    """
    module, _, klass = name.rpartition('.')
    mod = import_module(module)
    return getattr(mod, klass)