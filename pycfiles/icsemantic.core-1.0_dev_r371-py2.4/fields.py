# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/core/content/fields.py
# Compiled at: 2008-10-06 10:31:08
"""
@author: Juan Pablo Gimenez
@contact: jpg@rcom.com.ar
"""
__author__ = 'Juan Pablo Gimenez <jpg@rcom.com.ar>'
__docformat__ = 'plaintext'
import re
from zope.interface import implements
from icsemantic.core.interfaces import IFieldEmptiness

class TextFieldEmptiness(object):
    __module__ = __name__
    implements(IFieldEmptiness)

    def __init__(self, field):
        """
        Initialize our adapter
        """
        self.field = field

    def __call__(self, instance):
        value = self.field.get(instance)
        st = re.sub('<[^>]*>', '', value)
        st = re.sub('\\W', '', st)
        if len(st) > 0:
            return False
        else:
            return True


class FieldEmptiness(object):
    __module__ = __name__
    implements(IFieldEmptiness)

    def __init__(self, field):
        """
        Initialize our adapter
        """
        self.field = field

    def __call__(self, instance):
        value = self.field.get(instance)
        if value:
            return False
        else:
            return True