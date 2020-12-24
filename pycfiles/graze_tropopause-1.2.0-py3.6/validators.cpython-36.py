# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tropopause/validators.py
# Compiled at: 2018-02-02 11:23:12
# Size of source mod 2**32: 262 bytes
import re

def valid_url(url):
    regex = '(https?:\\/\\/)?([\\da-z\\.-]+)\\.([a-z\\.]{2,6})([\\/\\w \\.-]*)*\\/?$'
    valid_url_re = re.compile(regex)
    if valid_url_re.match(url):
        return url
    raise ValueError('%s is not a valid url', url)