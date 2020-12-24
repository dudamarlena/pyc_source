# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/__init__.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1318 bytes
"""PyAMS_utils package

PyAMS generic modules
"""
from zope.schema.fieldproperty import FieldProperty
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_utils')

def get_field_doc(self):
    """Try to get FieldProperty field docstring from field interface"""
    field = self._FieldProperty__field
    if field.title:
        if field.description:
            return '{0}: {1}'.format(field.title, field.description)
        return field.title
    return super(self.__class__, self).__doc__


FieldProperty.__doc__ = property(get_field_doc)

def includeme(config):
    """pyams_utils features include"""
    from .include import include_package
    include_package(config)