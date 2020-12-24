# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/labbook/mypackage.py
# Compiled at: 2015-06-01 23:44:29
"""
labbook.py

After modifying this file don't forget to modify __init__.py to expose your package's API.
"""

def a_function_of_mine():
    """
    This function returns the string 'result'.
    """
    return 'result'


class MyClass:
    """
    This is a class that should be documented.
    """

    def a_method_of_mine(self):
        """
        Please document public methods as well.
        """
        return 'another result'