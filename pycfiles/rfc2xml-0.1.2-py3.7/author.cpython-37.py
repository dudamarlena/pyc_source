# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/author.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 1117 bytes
from lxml import etree
from . import Element
from .organization import Organization

class Author(Element):
    tag_name = 'author'
    tag_name: str
    initials = None
    initials: str
    surname = None
    surname: str
    organization = None
    organization: 'Organization'
    role = None
    role: str

    def __init__(self, initials=None, surname=None, organization=None, role=None):
        super().__init__()
        self.initials = initials
        self.surname = surname
        self.organization = organization
        self.role = role

    def get_attributes(self):
        attributes = {}
        if self.initials is not None:
            attributes['initials'] = self.initials
        if self.surname is not None:
            attributes['surname'] = self.surname
        if self.role is not None:
            attributes['role'] = self.role
        return attributes

    def to_xml(self):
        element = etree.Element(str(self.tag_name), self.get_attributes())
        if self.organization is not None:
            element.append(self.organization.to_xml())
        self.children_to_xml(element)
        return element