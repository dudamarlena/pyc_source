# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/base/base.py
# Compiled at: 2015-11-16 08:17:20
__doc__ = '\nPyLEMS base class.\n\n@author: Gautham Ganapathy\n@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)\n@contact: gautham@lisphacker.org\n'
import copy

class LEMSBase(object):
    """
    Base object for PyLEMS.
    """

    def copy(self):
        return copy.deepcopy(self)

    def toxml(self):
        return ''