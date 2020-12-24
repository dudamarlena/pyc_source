# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\hooks.py
# Compiled at: 2011-07-08 11:39:35
"""Standard TurboGears request hooks for CherryPy."""
__all__ = [
 'NestedVariablesHook']
from cherrypy import request
from formencode.variabledecode import NestedVariables

def NestedVariablesHook():
    """Request filter for handling nested variables.

    Turns request parameters with names in special dotted notation into
    nested dictionaries via the FormEncode NestedVariables validator.

    Stores the original parameters in the 'original_params' attribute.

    """
    try:
        params = request.params
    except AttributeError:
        pass
    else:
        request.original_params = params
        request.params = NestedVariables.to_python(params or {})