# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/validator.py
# Compiled at: 2014-01-02 16:06:37
# Size of source mod 2**32: 1358 bytes
from wtforms.validators import Email, URL

def validate_email(email):
    """ 
        Validates an email 
    
        Returns True if valid and False if invalid
    """
    email_re = Email().regex
    result = email_re.match(email)
    if result is None:
        return False
    else:
        return result.string


def validate_url(url):
    """
        Validates a url

        Returns True if valid and False if invalid
    """
    url_re = URL().regex
    result = url_re.match(url)
    if result is None:
        return False
    else:
        return result.string