# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auction/utils/generic.py
# Compiled at: 2013-04-22 04:27:13
from auction.models.bidbasket import BidBasket
from django.contrib.auth.models import AnonymousUser

def get_bidbasket_from_database(request):
    try:
        return BidBasket.objects.filter(user=request.user)[0]
    except Exception as e:
        return False


def get_or_create_bidbasket(request, save=False):
    """
    Return bidbasket for current visitor.

    Requires a logged in user.

    If ``save`` is True, bidbasket object will be explicitly saved.
    """
    bidbasket = None
    if not hasattr(request, '_bidbasket'):
        bidbasket = None
        is_logged_in = request.user and not isinstance(request.user, AnonymousUser)
        if is_logged_in:
            bidbasket = get_bidbasket_from_database(request)
            if bidbasket:
                request.session['bidbasket_id'] = bidbasket.pk
            else:
                bidbasket = BidBasket(user=request.user)
        if save and not bidbasket.pk:
            bidbasket.save()
            request.session['bidbasket_id'] = bidbasket.pk
        setattr(request, '_bidbasket', bidbasket)
    bidbasket = getattr(request, '_bidbasket')
    return bidbasket


def get_current_time():
    import datetime
    try:
        from django.utils.timezone import utc
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
    except ImportError:
        now = datetime.datetime.utcnow()

    return now