# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/behaviors.py
# Compiled at: 2018-04-05 17:06:56
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import provider

@provider(IFormFieldProvider)
class IRichPreview(model.Schema):
    """Rich Link Preview behavior."""
    pass