# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\an_example_pypi_project\useful.py
# Compiled at: 2009-11-06 00:28:50
"""A very useful module indeed. 

"""

def public_fn_with_docstring():
    """
    """
    pass


def public_fn_without_docstring():
    return True


def _private_fn_with_docstring():
    """I have a docstring, but won't be imported if you just use :members:"""
    pass