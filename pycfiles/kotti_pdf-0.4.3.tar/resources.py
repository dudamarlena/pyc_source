# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_pdf/kotti_pdf/resources.py
# Compiled at: 2017-05-11 21:30:45
"""
Created on 2015-12-16
:author: Andreas Kaiser (disko@binary-punks.com)
"""
from kotti.resources import Content
from kotti.resources import File
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from zope.interface import implementer
from kotti_pdf import _
from kotti_pdf.interfaces import IPDF

@implementer(IPDF)
class PDF(File):
    """PDF is a specialized version of :class:`~kotti.resources.File`, that
    adds thumbnails and has different views.
    """
    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)
    type_info = Content.type_info.copy(name='PDF', title=_('PDF'), add_view='add_pdf', addable_to=[
     'Document'], selectable_default_views=[], uploadable_mimetypes=[
     'application/pdf'])