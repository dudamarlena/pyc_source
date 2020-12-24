# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/procblock/run/code_python.py
# Compiled at: 2010-10-15 02:02:13
"""
code_python

Import python modules to execute procblock Code with this library.

TODO(g): Ensure output PYC files are unique and never clobber each other.
"""
import imp, py_compile, os, sys, logging
from unidist.log import log
from unidist import sharedstate

def GetPythonScriptModule(script_filename):
    """Will return a Python module for this script_id, or None."""
    name = os.path.basename(script_filename)
    path = os.path.dirname(script_filename)
    if name.endswith('.py'):
        name = name[:-3]
    else:
        log('Script is not a python text file or is improperly named: %s' % script_filename, logging.CRITICAL)
        return
    sys.path.append(path)
    suffix_description = (
     '.py', 'r', imp.PY_SOURCE)
    fp = None
    try:
        try:
            compiled_filename = '%sc' % script_filename
            path = os.path.dirname(compiled_filename)
            module_name = os.path.basename(compiled_filename)
            py_compile.compile(script_filename, compiled_filename)
            fp = open(compiled_filename, 'rb')
            suffix_description = ('.pyc', 'rb', imp.PY_COMPILED)
            script_module = imp.load_module(module_name, fp, path, suffix_description)
            sharedstate.Set('__internals.python', script_filename, script_module)
            return script_module
        except ImportError, e:
            log('Failed to import script: %s: %s' % (
             os.path.abspath(script_filename), e), logging.CRITICAL)
        except Exception, e:
            log('Failed to import script for non-import reasons: %s: %s' % (
             script_filename, e), logging.CRITICAL)

    finally:
        if fp:
            fp.close()

    return