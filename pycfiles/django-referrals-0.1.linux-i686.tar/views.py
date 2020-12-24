# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/magikally/lib/python2.7/site-packages/referrals/views.py
# Compiled at: 2011-12-28 13:46:21
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf import settings
from referrals.models import Referral
from referrals.session import ReferralSessionManager

def refer(request, unique_key):
    referral = get_object_or_404(Referral, unique_key=unique_key)
    session = ReferralSessionManager(request)
    session['referral_id'] = referral.id
    return redirect(settings.REFERRAL_REDIRECT_URL)