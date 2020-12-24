# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/accountings/templatetags/accounting_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 702 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('accountings/acct_entry_item.html', takes_context=True)
def acct_entry_item(context, acct_entry, entry_class=''):
    acct_trans = acct_entry.trans.all()
    for acct_tran in acct_trans:
        if acct_tran.amount > 0:
            context['total_debit'] += acct_tran.amount
        if acct_tran.amount < 0:
            context['total_credit'] += abs(acct_tran.amount)

    context.update({'acct_trans':acct_trans, 
     'entry_class':entry_class})
    return context