# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\an_example_pypi_project\useful.py
# Compiled at: 2009-11-06 00:28:50
__doc__ = 'A very useful module indeed. \n\n\n\n'

def public_fn_with_docstring():
    """
    """
    pass


def public_fn_without_docstring():
    return True


def _private_fn_with_docstring():
    """I have a docstring, but won't be imported if you just use :members:"""
    pass