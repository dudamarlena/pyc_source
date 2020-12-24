# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/views.py
# Compiled at: 2015-03-06 05:08:58
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from post_office import mail
from post_office.models import EmailTemplate
from .utils import decode_data
from .models import SubscriptionSettings

def unsubscribe(request, hashed, data):
    try:
        username, email = decode_data(hashed, data)
    except Exception:
        raise Http404

    try:
        subscription = SubscriptionSettings.objects.get(user__username=username, user__email=email)
    except SubscriptionSettings.DoesNotExist as e:
        raise Http404

    if not request.POST:
        context = {'user': subscription.user, 'cancel_url': '/'}
        return render(request, 'mass_post_office/unsubscribe.html', context)
    if 'is_unsubscribed' not in request.POST:
        return redirect('/')
    subscription.subscribed = False
    subscription.save()
    try:
        mail.from_template(settings.DEFAULT_FROM_EMAIL, subscription.user.email, template='post_office/canceled_subscription', context={'user': subscription.user})
    except EmailTemplate.DoesNotExist as e:
        pass

    return redirect(reverse('mass_post_office:unsubscribed'))


def unsubscribed(request):
    context = {}
    return render(request, 'mass_post_office/complete.html', context)