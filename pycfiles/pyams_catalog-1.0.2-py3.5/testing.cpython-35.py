# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_catalog/testing.py
# Compiled at: 2020-02-21 06:54:32
# Size of source mod 2**32: 1672 bytes
"""PyAMS_catalog.testing module

Package testing utilities.
"""
import sys
from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty
from pyams_i18n.schema import I18nTextLineField
__docformat__ = 'restructuredtext'
if sys.argv[(-1)].endswith('/bin/test'):

    class IContentInterface(Interface):
        __doc__ = 'Content interface'
        value = TextLine(title='Value property')


    @implementer(IContentInterface)
    class MyContent(Persistent, Contained):
        __doc__ = 'Content persistent class'
        value = FieldProperty(IContentInterface['value'])


    class MyOtherContent(Persistent, Contained):
        __doc__ = 'Other content class'
        value = 'Other content value'


    class II18nContentInterface(Interface):
        __doc__ = 'I18n content interface'
        i18n_value = I18nTextLineField(title='I18n value property')


    @implementer(II18nContentInterface)
    class I18nContent(Persistent, Contained):
        __doc__ = 'I18n content class'
        i18n_value = FieldProperty(II18nContentInterface['i18n_value'])