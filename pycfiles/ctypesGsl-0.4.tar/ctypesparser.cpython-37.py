# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/parser/ctypesparser.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 8138 bytes
__doc__ = "\nctypesgen.parser.ctypesparser contains a class, CtypesParser, which is a\nsubclass of ctypesgen.parser.cparser.CParser. CtypesParser overrides the\nhandle_declaration() method of CParser. It turns the low-level type declarations\nproduced by CParser into CtypesType instances and breaks the parser's general\ndeclarations into function, variable, typedef, constant, and type descriptions.\n"
__docformat__ = 'restructuredtext'
__all__ = [
 'CtypesParser']
from ..ctypedescs import *
from ..expressions import *
from .cparser import *
from .cdeclarations import *

def make_enum_from_specifier(specifier):
    tag = specifier.tag
    enumerators = []
    last_name = None
    for e in specifier.enumerators:
        if e.expression:
            value = e.expression
        elif last_name:
            value = BinaryExpressionNode('addition', lambda x, y: x + y, '(%s + %s)', (False,
                                                                                       False), IdentifierExpressionNode(last_name), ConstantExpressionNode(1))
        else:
            value = ConstantExpressionNode(0)
        enumerators.append((e.name, value))
        last_name = e.name

    return CtypesEnum(tag, enumerators, src=(specifier.filename, specifier.lineno))


def get_decl_id(decl):
    """Return the identifier of a given declarator"""
    while isinstance(decl, Pointer):
        decl = decl.pointer

    p_name = ''
    if decl is not None:
        if decl.identifier is not None:
            p_name = decl.identifier
    return p_name


class CtypesParser(CParser):
    """CtypesParser"""

    def __init__(self, options):
        super(CtypesParser, self).__init__(options)
        self.type_map = ctypes_type_map
        if not options.no_python_types:
            self.type_map.update(ctypes_type_map_python_builtin)

    def make_struct_from_specifier(self, specifier):
        variety = {True:'union',  False:'struct'}[specifier.is_union]
        tag = specifier.tag
        if specifier.declarations:
            members = []
            for declaration in specifier.declarations:
                t = self.get_ctypes_type((declaration.type),
                  (declaration.declarator), check_qualifiers=True)
                declarator = declaration.declarator
                if declarator is None:
                    name = None
                else:
                    while declarator.pointer:
                        declarator = declarator.pointer

                    name = declarator.identifier
                members.append((name, remove_function_pointer(t)))

        else:
            members = None
        return CtypesStruct(tag,
          (specifier.attrib), variety, members, src=(specifier.filename, specifier.lineno))

    def get_ctypes_type(self, typ, declarator, check_qualifiers=False):
        signed = True
        typename = 'int'
        longs = 0
        t = None
        for specifier in typ.specifiers:
            if isinstance(specifier, StructTypeSpecifier):
                t = self.make_struct_from_specifier(specifier)
            elif isinstance(specifier, EnumSpecifier):
                t = make_enum_from_specifier(specifier)
            elif specifier == 'signed':
                signed = True
            elif specifier == 'unsigned':
                signed = False
            elif specifier == 'long':
                longs += 1
            else:
                typename = str(specifier)

        if not t:
            if (typename, signed, longs) in self.type_map:
                t = CtypesSimple(typename, signed, longs)
            elif signed:
                t = longs or CtypesTypedef(typename)
            else:
                name = ' '.join(typ.specifiers)
                if typename in [x[0] for x in self.type_map.keys()]:
                    error = 'Ctypes does not support the type "%s".' % name
                else:
                    error = 'Ctypes does not support adding additional specifiers to typedefs, such as "%s"' % name
                t = CtypesTypedef(name)
                t.error(error, cls='unsupported-type')
            if declarator:
                if declarator.bitfield:
                    t = CtypesBitfield(t, declarator.bitfield)
        qualifiers = []
        qualifiers.extend(typ.qualifiers)
        while declarator and declarator.pointer:
            if declarator.parameters is not None:
                variadic = '...' in declarator.parameters
                params = []
                for param in declarator.parameters:
                    if param == '...':
                        break
                    param_name = get_decl_id(param.declarator)
                    ct = self.get_ctypes_type(param.type, param.declarator)
                    ct.identifier = param_name
                    params.append(ct)

                t = CtypesFunction(t, params, variadic)
            a = declarator.array
            while a:
                t = CtypesArray(t, a.size)
                a = a.array

            qualifiers.extend(declarator.qualifiers)
            t = CtypesPointer(t, tuple(typ.qualifiers) + tuple(declarator.qualifiers))
            declarator = declarator.pointer

        if declarator:
            if declarator.parameters is not None:
                variadic = '...' in declarator.parameters
                params = []
                for param in declarator.parameters:
                    if param == '...':
                        break
                    param_name = get_decl_id(param.declarator)
                    ct = self.get_ctypes_type(param.type, param.declarator)
                    ct.identifier = param_name
                    params.append(ct)

                t = CtypesFunction(t, params, variadic, declarator.attrib)
        if declarator:
            a = declarator.array
            while a:
                t = CtypesArray(t, a.size)
                a = a.array

        if isinstance(t, CtypesPointer):
            if isinstance(t.destination, CtypesSimple):
                if t.destination.name == 'char':
                    if t.destination.signed:
                        t = CtypesSpecial('String')
        return t

    def handle_declaration(self, declaration, filename, lineno):
        t = self.get_ctypes_type(declaration.type, declaration.declarator)
        if type(t) in (CtypesStruct, CtypesEnum):
            self.handle_ctypes_new_type(remove_function_pointer(t), filename, lineno)
        else:
            declarator = declaration.declarator
            if declarator is None:
                return
                while declarator.pointer:
                    declarator = declarator.pointer

                name = declarator.identifier
                if declaration.storage == 'typedef':
                    self.handle_ctypes_typedef(name, remove_function_pointer(t), filename, lineno)
            elif type(t) == CtypesFunction:
                attrib = Attrib(t.attrib)
                attrib.update(declaration.attrib)
                self.handle_ctypes_function(name, t.restype, t.argtypes, t.errcheck, t.variadic, attrib, filename, lineno)
            elif declaration.storage != 'static':
                self.handle_ctypes_variable(name, t, filename, lineno)

    def handle_ctypes_new_type(self, ctype, filename, lineno):
        pass

    def handle_ctypes_typedef(self, name, ctype, filename, lineno):
        pass

    def handle_ctypes_function(self, name, restype, argtypes, errcheck, variadic, attrib, filename, lineno):
        pass

    def handle_ctypes_variable(self, name, ctype, filename, lineno):
        pass