# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_docit/kotti_docit/resources.py
# Compiled at: 2016-10-10 16:19:10
"""
Created on 2016-09-20
:author: Oshane Bailey (oshane@alteroo.com)
"""
from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Document
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from zope.interface import implements
from kotti_docit import _

class AdminManual(Document):
    """ Documents that are only visible by admins. """
    implements(IDefaultWorkflow)
    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    type_info = Document.type_info.copy(name='AdminManual', title=_('Admin Manual'), add_view='add_admin_manual', addable_to=[
     'Document'])