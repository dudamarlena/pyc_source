# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/utils/unifying.py
# Compiled at: 2015-08-17 17:37:49
"""
Библиотека с функциями унификации данных разных форматов
"""
try:
    import phonenumbers as pn
    from phonenumbers.phonenumberutil import NumberParseException
except ImportError:
    pass

def unify_email(origin_email):
    if not origin_email or '@' not in origin_email[1:-3]:
        return None
    user, domain = origin_email.strip().rsplit('@', 1)
    user = user.split('+')[0]
    email = ('@').join([user, domain])
    email = email.lower()
    return email


def unify_phone(origin_phone):
    try:
        try:
            phone = pn.parse(origin_phone)
        except NumberParseException:
            phone = pn.parse(origin_phone, 'RU')

        return pn.format_number(phone, pn.PhoneNumberFormat.INTERNATIONAL)
    except NameError:
        raise ImportError('django-phonenumber-field module is not available')