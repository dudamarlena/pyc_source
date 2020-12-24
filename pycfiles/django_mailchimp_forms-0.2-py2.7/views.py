# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_mailchimp_forms/views.py
# Compiled at: 2010-11-29 14:27:26
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from chimpy.chimpy import ChimpyException
from json import JSONEncoder
from django_mailchimp_forms.utils import register_user, unregister_user

@require_POST
@login_required
def chimpy_register(request, redirect_field='next'):
    if request.is_ajax():
        try:
            register_user(request.user)
            message = _('You have registered to our mailing list')
            success = True
        except Exception as e:
            message = _('Something went wrong: %s' % e[0])
            success = False

        json_dict = {'success': success, 'message': message}
        enc = JSONEncoder()
        return HttpResponse(enc.encode(json_dict), mimetype='application/json')
    else:
        redirect_to = request.GET[redirect_field]
        try:
            register_user(request.user)
            request.user.message_set.create(message=_('You have registered to our mailing list'))
        except Exception as e:
            request.user.message_set.create(message=_('Something went wrong: %s' % e[0]))

        return redirect(redirect_to)


@require_POST
@login_required
def chimpy_unregister(request, redirect_field='next'):
    if request.is_ajax():
        try:
            unregister_user(request.user)
            message = _('You have been removed from our mailing list')
            success = True
        except ChimpyException as e:
            message = _('Something went wrong: %s' % e[0])
            success = False

        json_dict = {'success': success, 'message': message}
        enc = JSONEncoder()
        return HttpResponse(enc.encode(json_dict), mimetype='application/json')
    else:
        redirect_to = request.GET[redirect_field]
        try:
            unregister_user(request.user)
            request.user.message_set.create(message=_('You have been removed our mailing list'))
        except ChimpyException as e:
            request.user.message_set.create(message=_('Something went wrong: %s' % e[0]))

        return redirect(redirect_to)