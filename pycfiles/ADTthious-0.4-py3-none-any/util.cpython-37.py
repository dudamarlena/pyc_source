# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tamell/code/adtpulsepy/adtpulsepy/helpers/util.py
# Compiled at: 2018-10-26 17:20:41
# Size of source mod 2**32: 453 bytes
__doc__ = ' Simple util package'
import re, json

def load_dirty_json(dirty_json):
    """Takes JSON returned from ADT and makes it valid python JSON"""
    regex_replace = [
     ('(\\\\)', '\\\\\\\\'), ("([ \\{,:\\[])(u)?'([^']+)'", '\\1"\\3"'), (' False([, \\}\\]])', ' false\\1'), (' True([, \\}\\]])', ' true\\1')]
    for req, sub in regex_replace:
        dirty_json = re.sub(req, sub, dirty_json)

    clean_json = json.loads(dirty_json)
    return clean_json