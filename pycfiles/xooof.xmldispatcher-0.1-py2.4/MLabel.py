# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/classinfo/MLabel.py
# Compiled at: 2008-10-01 10:39:40
from xooof.xmlstruct.xmlstruct import XMLStructBase, XMLStructBase_C
from xooof.xmlstruct.metafield import *
from xooof.xmlstruct.typeinfo import *

class MLabel(XMLStructBase):
    __module__ = __name__
    _metaStruct = None

    def _getMetaStruct(cls):
        if cls._metaStruct is None:
            cls._metaStruct = MLabel_M()
        return cls._metaStruct

    _getMetaStruct = classmethod(_getMetaStruct)


class MLabel_C(XMLStructBase_C):
    __module__ = __name__
    _itemKlass = MLabel


class MLabel_M:
    __module__ = __name__
    _xsNamespaceURI = 'http://xmlcatalog/catalog/spectools/class/classinfo' or None

    def __init__(self):
        self._lfields = []
        self._dfields = {}
        fname = 'lang'
        fmeta = MetaVField(MLabel_M._xsNamespaceURI, TypeInfo_string(2, 2, None), 0, MetaVField.SERIALIZE_element)
        self._lfields.append((fname, fmeta))
        self._dfields[fname] = fmeta
        fname = 'descr'
        fmeta = MetaVField(MLabel_M._xsNamespaceURI, TypeInfo_string(1, None, None), 1, MetaVField.SERIALIZE_element)
        self._lfields.append((fname, fmeta))
        self._dfields[fname] = fmeta
        return