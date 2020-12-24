# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/profiles/templatetags/profile_filters.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 503 bytes
from django.db.models import Q
from django.template import Library
from tendenci.apps.invoices.models import Invoice
register = Library()

@register.filter
def allow_edit_by(profile, user):
    """
    Check if the profile allows to be edited by the user. Returns True/False.
    """
    return profile.allow_edit_by(user)


@register.filter
def invoice_count(user):
    inv_count = Invoice.objects.filter(Q(creator=user) | Q(owner=user) | Q(bill_to_email=(user.email))).count()
    return inv_count