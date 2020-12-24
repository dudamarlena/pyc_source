# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/FinisAfricae/content/LendableObject.py
# Compiled at: 2007-11-27 13:05:16
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import CatalogTool
from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from Acquisition import aq_parent
from Acquisition import aq_inner
from zExceptions import NotFound
from Products.Archetypes.public import registerType
from Products.Archetypes.public import Schema
from Products.Archetypes.public import BaseSchema
from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import DisplayList
from Products.FinisAfricae.interfaces.FinisAfricaeLendableObject import IFinisAfricaeLendableObject
from Products.FinisAfricae.config import *

class LendableObject(BaseContent):
    """A lendable Object"""
    security = ClassSecurityInfo()
    meta_type = 'LendableObject'
    portal_type = 'LendableObject'
    archetype_name = 'Lendable Object'
    __implements__ = IFinisAfricaeLendableObject


registerType(LendableObject, PROJECT_NAME)