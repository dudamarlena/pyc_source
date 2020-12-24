# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/accounts/templatetags/account_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 373 bytes
from django.template import Library
from tendenci.apps.accounts.forms import LoginForm
register = Library()

@register.inclusion_tag('accounts/login_form.html', takes_context=True)
def login_form(context, login_button_value=None):
    form = LoginForm()
    context.update({'form':form, 
     'login_button_value':login_button_value})
    return context