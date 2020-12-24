# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/structOM.py
# Compiled at: 2008-10-01 10:40:59


class Struct:
    __module__ = __name__

    def __init__(self):
        self.specFile = None
        self.descr = []
        self.doc = []
        self.fields = []
        self.vfields = []
        self.vlfields = []
        self.gfields = []
        self.glfields = []
        self.xmlfields = []
        self.validate = []
        self.className = None
        self.baseClass = None
        self.structNs = None
        return

    def __repr__(self):
        return "Struct instance class='%s',baseClass='%s'" % (self.className, self.baseClass)

    def validateStruct(self):
        """TODO
           - validate name of Struct [A-Za-z][A-Za-z0-9]*
           - exclude all keywords from all programming languages
             (warning only, maybe, because struct2xxx should escape
             keywords)
           - (descr and doc for each language given as parameter ?)
           - if specs is given :
             * gfield exists
             * glfield exists
           - loops in subclasses
        """
        raise RuntimeError('not implemented')


class Field(object):
    __module__ = __name__
    VFIELD = 0
    GFIELD = 1
    VLFIELD = 2
    GLFIELD = 3
    XMLFIELD = 4

    def __init__(self):
        self.attrib = {}


class Vfield(Field):
    __module__ = __name__
    SERIALIZE_ELEMENT = 'element'
    SERIALIZE_ATTRIBUTE = 'attribute'
    SERIALIZE_PCDATA = 'pcdata'
    fieldType = Field.VFIELD

    def __init__(self):
        super(Vfield, self).__init__()
        self.descr = []
        self.datatype = None
        self.default = None
        self.doc = []
        self.validate = []
        self.name = None
        self.mandatory = 1
        self.serialize = Vfield.SERIALIZE_ELEMENT
        return

    def __repr__(self):
        return "Vfield instance name='%s',mandatory='%s', serialize = '%s',datatype='%s',default='%s'" % (self.name, self.mandatory, self.serialize, self.datatype, self.default)


class Vlfield(Field):
    __module__ = __name__
    fieldType = Field.VLFIELD

    def __init__(self):
        super(Vlfield, self).__init__()
        self.descr = []
        self.datatype = None
        self.default = None
        self.doc = []
        self.validate = []
        self.name = None
        self.maxOccur = None
        self.minOccur = None
        return

    def __repr__(self):
        return "Vlfield instance name='%s',datatype='%s',maxOccur='%s',minOccur='%s'" % (self.name, self.datatype, self.maxOccur, self.minOccur)


class Gfield(Field):
    __module__ = __name__
    fieldType = Field.GFIELD

    def __init__(self):
        super(Gfield, self).__init__()
        self.descr = []
        self.doc = []
        self.validate = []
        self.name = None
        self.mandatory = 1
        self.className = None
        return

    def __repr__(self):
        return "Gfield instance name='%s',mandatory='%s', class = '%s'" % (self.name, self.mandatory, self.className)


class Glfield(Field):
    __module__ = __name__
    fieldType = Field.GLFIELD

    def __init__(self):
        super(Glfield, self).__init__()
        self.descr = []
        self.doc = []
        self.validate = []
        self.name = None
        self.className = None
        self.maxOccur = None
        self.minOccur = None
        return

    def __repr__(self):
        return "Glfield instance name='%s',class='%s',minOccur='%s',maxOccur='%s'" % (self.name, self.className, self.minOccur, self.maxOccur)


class Xmlfield(Field):
    __module__ = __name__
    fieldType = Field.XMLFIELD

    def __init__(self):
        super(Xmlfield, self).__init__()
        self.descr = []
        self.doc = []
        self.validate = []
        self.name = None
        self.mandatory = 1
        return

    def __repr__(self):
        return "Gfield instance name='%s',mandatory='%s'" % (self.name, self.mandatory)


class Datatype:
    __module__ = __name__
    DATATYPES = ('tstring', 'tint', 'tdecimal', 'tboolean', 'tcode', 'tdatetime', 'ttime',
                 'tdate', 'tbinary')

    def __init__(self):
        self.datatype = None
        self.maxLen = None
        self.minLen = 1
        self.regexp = None
        self.maxVal = None
        self.minVal = None
        self.fractionDigits = None
        self.name = None
        self.encoding = None
        self.choices = []
        self.attrib = {}
        return

    def __repr__(self):
        return "Datatype instance : datatype = '%s'" % self.datatype

    def __str__(self):
        return self.__repr__()


class Choice:
    __module__ = __name__

    def __init__(self):
        self.value = None
        self.descr = []
        self.doc = []
        return


class Validation:
    __module__ = __name__

    def __init__(self):
        self.language = None
        self.validation = None
        return


class StructValidationException:
    __module__ = __name__

    def __init__(self):
        self._list = []

    def appendMsg(self, msg):
        self._list.append(msg)

    def appendException(self, ex):
        self._list += ex._list

    def __repr__(self):
        return self._list.join('\n')