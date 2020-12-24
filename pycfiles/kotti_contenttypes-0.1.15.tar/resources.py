# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_contenttypes/kotti_contenttypes/resources.py
# Compiled at: 2017-05-11 13:58:54
"""
Created on 2016-10-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Document
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from zope.interface import implements
from kotti_pdf.resources import PDF
from kotti_contenttypes import _

class Folder(Document):
    """ A custom content type. """
    implements(IDefaultWorkflow)
    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    type_info = Document.type_info.copy(name='Folder', title=_('Folder'), add_view='add_folder', addable_to=[
     'Document', 'Folder'])