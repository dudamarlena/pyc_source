# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/magikally/lib/python2.7/site-packages/referrals/utils.py
# Compiled at: 2011-12-28 15:15:40
from referrals.models import Referral
from referrals.signals import sign_up
from referrals.session import ReferralSessionManager

def process_request(request, new_user):
    """If there is a referring user, add the new_user to it's referrals"""
    session = ReferralSessionManager(request)
    if 'referral_id' in session:
        referral = Referral.objects.get(id=session['referral_id'])
        referral.referred_users.add(new_user)
        sign_up.send(sender=referral, instance=new_user)