# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/acceptors/core/web_opr.py
# Compiled at: 2017-01-30 19:40:56
# Size of source mod 2**32: 980 bytes
from tokenquery.acceptors.core.string_opr import str_reg

def web_is_url(token_input):
    url_regex = '^((http[s]?|ftp):\\/)?\\/?([^:\\/\\s]+)((\\/\\w+)*\\/)([\\w\\-\\.]+[^#?\\s]+)(.*)?(#[\\w\\-]+)?$'
    return str_reg(token_input, url_regex)


def web_is_email(token_input):
    email_regex = '(^[mailto:]?[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)'
    return str_reg(token_input, email_regex)


def web_is_hex_code(token_input):
    hex_regex = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return str_reg(token_input, hex_regex)


def web_is_hashtag(token_input):
    if token_input[0] == '#' and ' ' not in token_input:
        return True
    else:
        return False


def web_is_emoji(token_input, operation_input):
    unicode_regex = '(<U\\\\+\\\\w+?>)'
    if str_reg(token_input, unicode_regex):
        return True
    else:
        emojicons = '(^|\\s)(:D|:\\/)(?=\\s|[^[:alnum:]+-]|$)'
        return str_reg(token_input, emojicons)
    return False