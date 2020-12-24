# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/beaker/interfaces.py
# Compiled at: 2014-11-26 06:50:06
from zope.session.interfaces import ISessionDataContainer
from zope.schema import Choice
from ztfy.beaker import _

class IBeakerSessionUtility(ISessionDataContainer):
    """Beaker session utility"""
    configuration_name = Choice(title=_('Beaker session configuration name'), description=_('Name of Beaker configuration utility'), vocabulary='ZTFY Beaker sessions configurations', required=False, default='')