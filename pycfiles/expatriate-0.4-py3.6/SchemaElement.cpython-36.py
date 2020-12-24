# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\SchemaElement.py
# Compiled at: 2018-01-18 12:31:54
# Size of source mod 2**32: 3838 bytes
import logging, os.path
from . import FORM_CHOICE_ENUMERATION
from ..decorators import *
from .AnnotationElement import AnnotationElement
from .AnyTypeType import AnyTypeType
from .AnyUriType import AnyUriType
from .AttributeGroupType import AttributeGroupType
from .AttributeType import AttributeType
from .ComplexTypeType import ComplexTypeType
from .ElementType import ElementType
from .GroupType import GroupType
from .IdType import IdType
from .ImportElement import ImportElement
from .IncludeElement import IncludeElement
from .NotationElement import NotationElement
from .RedefineElement import RedefineElement
from .SimpleTypeType import SimpleTypeType
from .TokenType import TokenType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='targetNamespace', type=AnyUriType)
@attribute(local_name='version', type=TokenType)
@attribute(local_name='finalDefault', enum=['#all', 'extension', 'restriction', 'list', 'union'])
@attribute(local_name='blockDefault', enum=['#all', 'extension', 'restriction', 'substitution'])
@attribute(local_name='attributeFormDefault', enum=FORM_CHOICE_ENUMERATION, default='unqualified')
@attribute(local_name='elementFormDefault', enum=FORM_CHOICE_ENUMERATION, default='unqualified')
@attribute(local_name='id', type=IdType)
@element(local_name='include', list='tags', cls=IncludeElement, min=0, max=None)
@element(local_name='import', list='tags', cls=ImportElement, min=0, max=None)
@element(local_name='redefine', list='tags', cls=RedefineElement, min=0, max=None)
@element(local_name='annotation', list='tags', cls=AnnotationElement, min=0, max=None)
@element(local_name='simpleType', list='tags', cls=SimpleTypeType, min=0, max=None)
@element(local_name='complexType', list='tags', cls=ComplexTypeType, min=0, max=None)
@element(local_name='group', list='tags', cls=GroupType, min=0, max=None)
@element(local_name='attributeGroup', list='tags', cls=AttributeGroupType, min=0, max=None)
@element(local_name='element', list='tags', cls=ElementType, min=0, max=None)
@element(local_name='attribute', list='tags', cls=AttributeType, min=0, max=None)
@element(local_name='notation', list='tags', cls=NotationElement, min=0, max=None)
class SchemaElement(AnyTypeType):

    def add_enumeration(self, name, enum):
        self._enumerations[name] = enum

    def add_tag_mapping(self, name, class_name):
        self._tag_mapping[name] = class_name

    def stub(self, path):
        self._enumerations = {}
        self._tag_mapping = {}
        for c in self.tags:
            if c.tag_name in ('simpleType', 'complexType', 'element'):
                c.stub(path, self)

        with open(os.path.join(path, '__init__.py'), 'w') as (f):
            f.write(STUB_HEADER)
            f.write('ELEMENT_MAP = {\n')
            for name in sorted(self._tag_mapping.keys()):
                f.write("    '{" + self.targetNamespace + '}' + name + "': '" + self._tag_mapping[name] + "',\n")

            f.write('}\n\n')
        logger.debug('Wrote __init__.py')