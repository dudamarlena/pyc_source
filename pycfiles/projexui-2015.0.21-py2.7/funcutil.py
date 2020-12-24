# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/funcutil.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = '\nFunction editing utilities\n'

def extract_keywords(func):
    """
    Parses the keywords from the given function.

    :param      func | <function>
    """
    if hasattr(func, 'im_func'):
        func = func.im_func
    try:
        return func.func_code.co_varnames[-len(func.func_defaults):]
    except (TypeError, ValueError, IndexError):
        return tuple()