# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/base/base.py
# Compiled at: 2015-11-16 08:17:20
"""
PyLEMS base class.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""
import copy

class LEMSBase(object):
    """
    Base object for PyLEMS.
    """

    def copy(self):
        return copy.deepcopy(self)

    def toxml(self):
        return ''