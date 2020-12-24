# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/medialog/boardfile/interfaces/publication.py
# Compiled at: 2011-11-28 04:21:33
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from medialog.boardfile import boardfileMessageFactory as _

class IPublication(Interface):
    """Publication content type"""
    publicationcategory = schema.TextLine(title=_('Publication Category'), required=True, description=_('Please select a category'))
    publicationtitle = schema.TextLine(title=_('Journal/Conference'), required=True, description=_('Name of Journal/Conference.'))
    authorlist = schema.Text(title=_('Authorlist'), required=True, description=_('List of Authors'))
    wp = schema.TextLine(title=_('WP'), required=True, description=_('Select one'))
    deliverable = schema.Float(title=_('Deliverable number'), required=False, description=_('The deliverable number'))
    publishingyear = schema.Int(title=_('Publishing Year'), required=True, description=_('Publishing Year'))