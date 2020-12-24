# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/skin/layer.py
# Compiled at: 2013-04-23 02:35:12
__docformat__ = 'restructuredtext'
from ztfy.appskin.layer import IAppLayer, IAppSkin
from zope.schema import TextLine
from ztfy.sendit import _

class ISenditLayer(IAppLayer):
    """Sendit browser layer"""
    pass


class ISenditSkin(IAppSkin, ISenditLayer):
    """Sendit browser skin"""
    name = TextLine(title=_('SendIt skin'))