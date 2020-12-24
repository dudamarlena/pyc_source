# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/ProjectName/projectname/lib/helpers.py
# Compiled at: 2007-09-06 07:54:15
"""
Helper functions

All names available in this module will be available under the Pylons h object.
"""
from webhelpers import *
from pylons.helpers import log, abort
from pylons.i18n import get_lang, set_lang

def get_object_or_404(model, **kw):
    """
    Returns object, or raises a 404 Not Found is object is not in db 
    Example: user = get_object_or_404(model.User, id = 1)
    """
    obj = model.get_by(**kw)
    if obj is None:
        abort(404)
    return obj