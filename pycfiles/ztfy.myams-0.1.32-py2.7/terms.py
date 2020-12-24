# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/myams/terms.py
# Compiled at: 2014-09-12 08:11:44
from z3c.form.interfaces import IWidget, IBoolTerms
from zope.schema.interfaces import IBool
from ztfy.myams.layer import MyAMSLayer
from z3c.form.term import BoolTerms as BaseBoolTerms
from zope.component import adapts
from zope.interface import implementsOnly, Interface
from ztfy.skin import _

class BoolTerms(BaseBoolTerms):
    """Default yes and no terms are used by default for IBool fields."""
    adapts(Interface, MyAMSLayer, Interface, IBool, IWidget)
    implementsOnly(IBoolTerms)
    trueLabel = _('yes')
    falseLabel = _('no')