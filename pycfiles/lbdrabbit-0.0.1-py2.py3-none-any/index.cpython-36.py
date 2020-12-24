# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/example/handlers/view/index.py
# Compiled at: 2019-10-05 15:01:50
# Size of source mod 2**32: 195 bytes
html = '\n<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<strong>Welcome to Index page</strong>\n</body>\n</html>\n'.strip()

def handler(event, context):
    return html