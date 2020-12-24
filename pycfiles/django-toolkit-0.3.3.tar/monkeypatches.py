# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/monkeypatches.py
# Compiled at: 2015-02-05 18:23:17
try:
    import moneyed as money
    from moneyed.localization import format_money
except ImportError:
    try:
        import money
        from money.localization import format_money
    except ImportError:
        money = None

def format_money_remove_aud(self, **kwargs):
    """
    Monkey patch money.Money.format so that the default currency (AUD) isn't displayed
    when calling Money.format()

    @author: Alex Hayes <alex.hayes@roi.com.au>
    """
    return format_money(self, **kwargs).replace('A$', '$')


if money:
    money.Money.format = format_money_remove_aud