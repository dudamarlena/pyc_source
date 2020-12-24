# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/ctypedescs.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 10781 bytes
__doc__ = '\nctypesgen.ctypedescs contains classes to represent a C type. All of them\nclasses are subclasses of CtypesType.\n\nUnlike in previous versions of ctypesgen, CtypesType and its subclasses are\ncompletely independent of the parser module.\n\nThe most important method of CtypesType and its subclasses is the py_string\nmethod. str(ctype) returns a string which, when evaluated in the wrapper\nat runtime, results in a ctypes type object.\n\nFor example, a CtypesType\nrepresenting an array of four integers could be created using:\n\n>>> ctype = CtypesArray(CtypesSimple("int",True,0),4)\n\nstr(ctype) would evaluate to "c_int * 4".\n'
import warnings
__docformat__ = 'restructuredtext'
ctypes_type_map = {('void', True, 0):'None', 
 ('int', True, 0):'c_int', 
 ('int', False, 0):'c_uint', 
 ('int', True, 1):'c_long', 
 ('int', False, 1):'c_ulong', 
 ('char', True, 0):'c_char', 
 ('char', False, 0):'c_ubyte', 
 ('short', True, 0):'c_short', 
 ('short', False, 0):'c_ushort', 
 ('float', True, 0):'c_float', 
 ('double', True, 0):'c_double', 
 ('double', True, 1):'c_longdouble', 
 ('int8_t', True, 0):'c_int8', 
 ('int16_t', True, 0):'c_int16', 
 ('int32_t', True, 0):'c_int32', 
 ('int64_t', True, 0):'c_int64', 
 ('uint8_t', True, 0):'c_uint8', 
 ('uint16_t', True, 0):'c_uint16', 
 ('uint32_t', True, 0):'c_uint32', 
 ('uint64_t', True, 0):'c_uint64', 
 ('_Bool', True, 0):'c_bool'}
ctypes_type_map_python_builtin = {('int', True, 2):'c_longlong', 
 ('int', False, 2):'c_ulonglong', 
 ('size_t', True, 0):'c_size_t', 
 ('apr_int64_t', True, 0):'c_int64', 
 ('off64_t', True, 0):'c_int64', 
 ('apr_uint64_t', True, 0):'c_uint64', 
 ('wchar_t', True, 0):'c_wchar', 
 ('ptrdiff_t', True, 0):'c_ptrdiff_t', 
 ('ssize_t', True, 0):'c_ptrdiff_t', 
 ('va_list', True, 0):'c_void_p'}

class CtypesTypeVisitor(object):

    def visit_struct(self, struct):
        pass

    def visit_enum(self, enum):
        pass

    def visit_typedef(self, name):
        pass

    def visit_error(self, error, cls):
        pass

    def visit_identifier(self, identifier):
        pass


def visit_type_and_collect_info(ctype):

    class Visitor(CtypesTypeVisitor):

        def visit_struct(self, struct):
            structs.append(struct)

        def visit_enum(self, enum):
            enums.append(enum)

        def visit_typedef(self, typedef):
            typedefs.append(typedef)

        def visit_error(self, error, cls):
            errors.append((error, cls))

        def visit_identifier(self, identifier):
            identifiers.append(identifier)

    structs = []
    enums = []
    typedefs = []
    errors = []
    identifiers = []
    v = Visitor()
    ctype.visit(v)
    return (
     structs, enums, typedefs, errors, identifiers)


def remove_function_pointer(t):
    if type(t) == CtypesPointer:
        if type(t.destination) == CtypesFunction:
            return t.destination
    if type(t) == CtypesPointer:
        t.destination = remove_function_pointer(t.destination)
        return t
    return t


class CtypesType(object):

    def __init__(self):
        super(CtypesType, self).__init__()
        self.errors = []

    def __repr__(self):
        return '<Ctype (%s) "%s">' % (type(self).__name__, self.py_string())

    def error(self, message, cls=None):
        self.errors.append((message, cls))

    def visit(self, visitor):
        for error, cls in self.errors:
            visitor.visit_error(error, cls)


class CtypesSimple(CtypesType):
    """CtypesSimple"""

    def __init__(self, name, signed, longs):
        super(CtypesSimple, self).__init__()
        self.name = name
        self.signed = signed
        self.longs = longs

    def py_string(self, ignore_can_be_ctype=None):
        return ctypes_type_map[(self.name, self.signed, self.longs)]


class CtypesSpecial(CtypesType):

    def __init__(self, name):
        super(CtypesSpecial, self).__init__()
        self.name = name

    def py_string(self, ignore_can_be_ctype=None):
        return self.name


class CtypesTypedef(CtypesType):
    """CtypesTypedef"""

    def __init__(self, name):
        super(CtypesTypedef, self).__init__()
        self.name = name

    def visit(self, visitor):
        if not self.errors:
            visitor.visit_typedef(self.name)
        super(CtypesTypedef, self).visit(visitor)

    def py_string(self, ignore_can_be_ctype=None):
        return self.name


class CtypesBitfield(CtypesType):

    def __init__(self, base, bitfield):
        super(CtypesBitfield, self).__init__()
        self.base = base
        self.bitfield = bitfield

    def visit(self, visitor):
        self.base.visit(visitor)
        super(CtypesBitfield, self).visit(visitor)

    def py_string(self, ignore_can_be_ctype=None):
        return self.base.py_string()


class CtypesPointer(CtypesType):

    def __init__(self, destination, qualifiers):
        super(CtypesPointer, self).__init__()
        self.destination = destination
        self.qualifiers = qualifiers

    def visit(self, visitor):
        if self.destination:
            self.destination.visit(visitor)
        super(CtypesPointer, self).visit(visitor)

    def py_string(self, ignore_can_be_ctype=None):
        return 'POINTER(%s)' % self.destination.py_string()


class CtypesArray(CtypesType):

    def __init__(self, base, count):
        super(CtypesArray, self).__init__()
        self.base = base
        self.count = count

    def visit(self, visitor):
        self.base.visit(visitor)
        if self.count:
            self.count.visit(visitor)
        super(CtypesArray, self).visit(visitor)

    def py_string(self, ignore_can_be_ctype=None):
        if self.count is None:
            return 'POINTER(%s)' % self.base.py_string()
        if type(self.base) == CtypesArray:
            return '(%s) * int(%s)' % (self.base.py_string(), self.count.py_string(False))
        return '%s * int(%s)' % (self.base.py_string(), self.count.py_string(False))


class CtypesNoErrorCheck(object):

    def py_string(self, ignore_can_be_ctype=None):
        return 'None'

    def __bool__(self):
        return False

    __nonzero__ = __bool__


class CtypesPointerCast(object):

    def __init__(self, target):
        self.target = target

    def py_string(self, ignore_can_be_ctype=None):
        return 'lambda v,*a : cast(v, {})'.format(self.target.py_string())


class CtypesFunction(CtypesType):

    def __init__(self, restype, parameters, variadic, attrib=dict()):
        super(CtypesFunction, self).__init__()
        self.restype = restype
        self.errcheck = CtypesNoErrorCheck()
        if type(self.restype) == CtypesPointer:
            if type(self.restype.destination) == CtypesSimple:
                if self.restype.destination.name == 'void':
                    self.restype = CtypesPointer(CtypesSpecial('c_ubyte'), ())
                    self.errcheck = CtypesPointerCast(CtypesSpecial('c_void_p'))
        elif self.restype.py_string() == 'POINTER(c_char)':
            if 'const' in self.restype.qualifiers:
                self.restype = CtypesSpecial('c_char_p')
            else:
                self.restype = CtypesSpecial('String')
        self.argtypes = [remove_function_pointer(p) for p in parameters]
        self.variadic = variadic
        self.attrib = attrib

    def visit(self, visitor):
        self.restype.visit(visitor)
        for a in self.argtypes:
            a.visit(visitor)

        super(CtypesFunction, self).visit(visitor)

    def py_string(self, ignore_can_be_ctype=None):
        return 'CFUNCTYPE(UNCHECKED(%s), %s)' % (
         self.restype.py_string(),
         ', '.join([a.py_string() for a in self.argtypes]))


last_tagnum = 0

def anonymous_struct_tag():
    global last_tagnum
    last_tagnum += 1
    return 'anon_%d' % last_tagnum


class CtypesStruct(CtypesType):

    def __init__(self, tag, attrib, variety, members, src=None):
        super(CtypesStruct, self).__init__()
        self.tag = tag
        self.attrib = attrib
        self.variety = variety
        self.members = members
        if not self.tag:
            self.tag = anonymous_struct_tag()
            self.anonymous = True
        else:
            self.anonymous = False
        if self.members == None:
            self.opaque = True
        else:
            self.opaque = False
        self.src = src

    def get_required_types(self):
        types = super(CtypesStruct, self).get_required_types()
        types.add((self.variety, self.tag))
        return types

    def visit(self, visitor):
        visitor.visit_struct(self)
        if not self.opaque:
            for name, ctype in self.members:
                ctype.visit(visitor)

        super(CtypesStruct, self).visit(visitor)

    def get_subtypes(self):
        if self.opaque:
            return set()
        return set([m[1] for m in self.members])

    def py_string(self, ignore_can_be_ctype=None):
        return '%s_%s' % (self.variety, self.tag)


last_tagnum = 0

def anonymous_enum_tag():
    global last_tagnum
    last_tagnum += 1
    return 'anon_%d' % last_tagnum


class CtypesEnum(CtypesType):

    def __init__(self, tag, enumerators, src=None):
        super(CtypesEnum, self).__init__()
        self.tag = tag
        self.enumerators = enumerators
        if not self.tag:
            self.tag = anonymous_enum_tag()
            self.anonymous = True
        else:
            self.anonymous = False
        if self.enumerators == None:
            self.opaque = True
        else:
            self.opaque = False
        self.src = src

    def visit(self, visitor):
        visitor.visit_enum(self)
        super(CtypesEnum, self).visit(visitor)

    def py_string(self, ignore_can_be_ctype=None):
        return 'enum_%s' % self.tag