# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chschw/Workspace/django/lab/django-cms/site/statify/utils.py
# Compiled at: 2013-04-24 04:02:44
import requests

def url_is_valid(url):
    valid_codes = [
     200, 301, 302]
    request = requests.get(url)
    if request.status_code in valid_codes:
        return True
    else:
        return False