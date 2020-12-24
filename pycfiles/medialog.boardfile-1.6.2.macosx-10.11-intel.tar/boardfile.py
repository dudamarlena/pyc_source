# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/medialog/boardfile/interfaces/boardfile.py
# Compiled at: 2011-10-07 04:21:09
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from medialog.boardfile import boardfileMessageFactory as _

class IBoardfile(Interface):
    """Boardfile content type"""
    wp = schema.TextLine(title=_('WP'), required=True, description=_('Select one'))
    file = schema.Bytes(title=_('File'), required=True, description=_('File to upload. If you have many, please zip them first'))