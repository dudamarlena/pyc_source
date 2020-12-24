# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/git/alphabuyer/.env/local/lib/python2.7/site-packages/ajax_forms/templatetags/jquery_validation.py
# Compiled at: 2017-05-12 13:29:54
import os
from django import template
import ajax_forms
register = template.Library()
VALIDATION_SCRIPT = None

def include_validation():
    global VALIDATION_SCRIPT
    if VALIDATION_SCRIPT is None:
        VALIDATION_SCRIPT = open(os.path.join(os.path.dirname(ajax_forms.__file__), 'media', 'ajax_forms', 'js', 'jquery-ajax-validation.js')).read()
    return '<script type="text/javascript">%s</script>' % VALIDATION_SCRIPT


register.simple_tag(include_validation)