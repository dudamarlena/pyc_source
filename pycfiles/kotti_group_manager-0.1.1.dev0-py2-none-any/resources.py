# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_group_manager/kotti_group_manager/resources.py
# Compiled at: 2018-09-19 03:25:35
"""
Created on 2018-09-19
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Document
from kotti.security import get_principals
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from zope.interface import implements
from kotti_group_manager import _

class GroupPage(Document):
    """ A custom content type. """
    implements(IDefaultWorkflow)
    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    group_name = Column(Unicode(100), ForeignKey('principals.name'))
    type_info = Document.type_info.copy(name='GroupPage', title=_('Group Page'), add_view='add_group_page', addable_to=[
     'Document', 'Content'])

    @property
    def group(self):
        principals = get_principals()
        group = principals.search(name=self.group_name).first()
        return group

    @property
    def group_id(self):
        return self.group_name.replace('group:', '')