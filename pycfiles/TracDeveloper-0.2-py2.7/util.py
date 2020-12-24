# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tracdeveloper/util.py
# Compiled at: 2011-09-06 06:16:46
import re
from genshi import HTML

def linebreaks(value):
    """Converts newlines in strings into <p> and <br />s."""
    if not value:
        return ''
    value = re.sub('\\r\\n|\\r|\\n', '\n', value)
    paras = re.split('\n{2,}', value)
    paras = [ '<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paras ]
    return HTML(('').join(paras))