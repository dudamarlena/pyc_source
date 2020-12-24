# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tamell/code/adtpulsepy/adtpulsepy/helpers/util.py
# Compiled at: 2018-10-26 17:20:41
# Size of source mod 2**32: 453 bytes
""" Simple util package"""
import re, json

def load_dirty_json(dirty_json):
    """Takes JSON returned from ADT and makes it valid python JSON"""
    regex_replace = [
     ('(\\\\)', '\\\\\\\\'), ("([ \\{,:\\[])(u)?'([^']+)'", '\\1"\\3"'), (' False([, \\}\\]])', ' false\\1'), (' True([, \\}\\]])', ' true\\1')]
    for req, sub in regex_replace:
        dirty_json = re.sub(req, sub, dirty_json)

    clean_json = json.loads(dirty_json)
    return clean_json