# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_migration/kotti_migration/resources.py
# Compiled at: 2017-05-22 09:12:51
"""
Created on 2017-05-22
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Content
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from zope.interface import implements
from kotti_migration import _

class CustomContent(Content):
    """ A custom content type. """
    implements(IDefaultWorkflow)
    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    custom_attribute = Column(Unicode(1000))
    type_info = Content.type_info.copy(name='CustomContent', title=_('CustomContent'), add_view='add_custom_content', addable_to=[
     'Document'], selectable_default_views=[
     (
      'alternative-view', _('Alternative view'))])

    def __init__(self, custom_attribute=None, **kwargs):
        """ Constructor

        :param custom_attribute: A very custom attribute
        :type custom_attribute: unicode

        :param **kwargs: Arguments that are passed to the base class(es)
        :type **kwargs: see :class:`kotti.resources.Content`
        """
        super(CustomContent, self).__init__(**kwargs)
        self.custom_attribute = custom_attribute