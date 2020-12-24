# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/admin/workspace/eclipse/smile-dev/happystamp/templatetags/happystamp_tags.py
# Compiled at: 2016-01-07 18:04:48
# Size of source mod 2**32: 872 bytes
from datetime import date
from mezzanine import template
from happystamp.models import Transaction
register = template.Library()

@register.inclusion_tag('includes/daily_metrics.html', takes_context=True)
def daily_metrics(context):
    """
    Renders the daily metrics for the admin dashboard widget.
    """
    query_set = Transaction.objects.filter(created__gt=date.today(), card__program__user=context.get('request', None).user)
    reward_count = query_set.filter(debit__gt=0).count()
    redeem_count = query_set.filter(credit__gt=0).count()
    context.update({'reward_count': reward_count,  'redeem_count': redeem_count})
    return context