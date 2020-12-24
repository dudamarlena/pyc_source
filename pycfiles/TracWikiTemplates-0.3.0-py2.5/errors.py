# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WikiTemplates/errors.py
# Compiled at: 2007-11-10 06:34:56
from trac.util import escape

def TemplatesError(message):
    """
    Class to output a pretty error.
    """
    html = '\n<div class="system-message">\n<strong>Wiki Templates Error:</strong>\n<pre>%(message)s</pre>\n</div>\n' % {'message': escape(message)}
    return html