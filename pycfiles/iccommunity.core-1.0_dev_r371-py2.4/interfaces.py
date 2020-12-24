# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/core/interfaces.py
# Compiled at: 2008-10-06 10:31:14
""" iccommunity.core interfaces.
"""
from zope import schema
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty
from iccommunity.core.i18n import _

class IicCommunitySite(Interface):
    """ represents a platecom installation, should be a local site
        with local components installed
    """
    __module__ = __name__


class IPlatecomConfiglet(Interface):
    """ platecom configlet
    """
    __module__ = __name__