# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/parser/datacollectingparser.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 12375 bytes
__doc__ = '\nDataCollectingParser subclasses ctypesparser.CtypesParser and builds Description\nobjects from the CtypesType objects and other information from CtypesParser.\nAfter parsing is complete, a DescriptionCollection object can be retrieved by\ncalling DataCollectingParser.data().\n'
from . import ctypesparser
from ..descriptions import *
from ..ctypedescs import *
from ..expressions import *
from ..messages import *
from tempfile import mkstemp
import os

class DataCollectingParser(ctypesparser.CtypesParser, ctypesparser.CtypesTypeVisitor):
    """DataCollectingParser"""

    def __init__(self, headers, options):
        super(DataCollectingParser, self).__init__(options)
        self.headers = headers
        self.options = options
        self.constants = []
        self.typedefs = []
        self.structs = []
        self.enums = []
        self.functions = []
        self.variables = []
        self.macros = []
        self.all = []
        self.output_order = []
        null = ConstantExpressionNode(None)
        nullmacro = ConstantDescription('NULL', null, ('<built-in>', 1))
        self.constants.append(nullmacro)
        self.all.append(nullmacro)
        self.output_order.append(('constant', nullmacro))
        self.saved_macros = []
        self.already_seen_structs = set()
        self.already_seen_opaque_structs = {}
        self.already_seen_enums = set()
        self.already_seen_opaque_enums = {}

    def parse(self):
        fd, fname = mkstemp(suffix='.h')
        with os.fdopen(fd, 'w') as (f):
            for header in self.options.other_headers:
                f.write('#include <%s>\n' % header)

            for header in self.headers:
                f.write('#include "%s"\n' % os.path.abspath(header))

            f.flush()
        try:
            super(DataCollectingParser, self).parse(fname, self.options.debug_level)
        finally:
            os.unlink(fname)

        for name, params, expr, (filename, lineno) in self.saved_macros:
            self.handle_macro(name, params, expr, filename, lineno)

    def handle_define_constant(self, name, expr, filename, lineno):
        self.saved_macros.append((name, None, expr, (filename, lineno)))

    def handle_define_unparseable(self, name, params, value, filename, lineno):
        if params:
            original_string = '#define %s(%s) %s' % (name, ','.join(params), ' '.join(value))
        else:
            original_string = '#define %s %s' % (name, ' '.join(value))
        macro = MacroDescription(name, params, None, src=(filename, lineno))
        macro.error(('Could not parse macro "%s"' % original_string), cls='macro')
        macro.original_string = original_string
        self.macros.append(macro)
        self.all.append(macro)
        self.output_order.append(('macro', macro))

    def handle_define_macro(self, name, params, expr, filename, lineno):
        self.saved_macros.append((name, params, expr, (filename, lineno)))

    def handle_undefine(self, macro, filename, lineno):
        self.saved_macros.append(('#undef', None, macro, (filename, lineno)))

    def handle_ctypes_typedef(self, name, ctype, filename, lineno):
        ctype.visit(self)
        typedef = TypedefDescription(name, ctype, src=(filename, repr(lineno)))
        self.typedefs.append(typedef)
        self.all.append(typedef)
        self.output_order.append(('typedef', typedef))

    def handle_ctypes_new_type(self, ctype, filename, lineno):
        if isinstance(ctype, ctypesparser.CtypesEnum):
            self.handle_enum(ctype, filename, lineno)
        else:
            self.handle_struct(ctype, filename, lineno)

    def handle_ctypes_function(self, name, restype, argtypes, errcheck, variadic, attrib, filename, lineno):
        restype.visit(self)
        for argtype in argtypes:
            argtype.visit(self)

        function = FunctionDescription(name,
          restype, argtypes, errcheck, variadic, attrib, src=(filename, repr(lineno)))
        self.functions.append(function)
        self.all.append(function)
        self.output_order.append(('function', function))

    def handle_ctypes_variable(self, name, ctype, filename, lineno):
        ctype.visit(self)
        variable = VariableDescription(name, ctype, src=(filename, repr(lineno)))
        self.variables.append(variable)
        self.all.append(variable)
        self.output_order.append(('variable', variable))

    def handle_struct(self, ctypestruct, filename, lineno):
        name = '%s %s' % (ctypestruct.variety, ctypestruct.tag)
        if name in self.already_seen_structs:
            return
        else:
            if ctypestruct.opaque:
                if name not in self.already_seen_opaque_structs:
                    struct = StructDescription((ctypestruct.tag),
                      (ctypestruct.attrib),
                      (ctypestruct.variety),
                      None,
                      True,
                      ctypestruct,
                      src=(
                     filename, str(lineno)))
                    self.already_seen_opaque_structs[name] = struct
                    self.structs.append(struct)
                    self.all.append(struct)
                    self.output_order.append(('struct', struct))
            else:
                for membername, ctype in ctypestruct.members:
                    ctype.visit(self)

                if name in self.already_seen_opaque_structs:
                    struct = self.already_seen_opaque_structs[name]
                    struct.opaque = False
                    struct.members = ctypestruct.members
                    struct.ctype = ctypestruct
                    struct.src = ctypestruct.src
                    self.output_order.append(('struct-body', struct))
                    del self.already_seen_opaque_structs[name]
                else:
                    struct = StructDescription((ctypestruct.tag),
                      (ctypestruct.attrib),
                      (ctypestruct.variety),
                      (ctypestruct.members),
                      False,
                      src=(
                     filename, str(lineno)),
                      ctype=ctypestruct)
                    self.structs.append(struct)
                    self.all.append(struct)
                    self.output_order.append(('struct', struct))
                    self.output_order.append(('struct-body', struct))
                self.already_seen_structs.add(name)

    def handle_enum(self, ctypeenum, filename, lineno):
        tag = ctypeenum.tag
        if tag in self.already_seen_enums:
            return
        else:
            if ctypeenum.opaque:
                if tag not in self.already_seen_opaque_enums:
                    enum = EnumDescription((ctypeenum.tag), None, ctypeenum, src=(filename, str(lineno)))
                    enum.opaque = True
                    self.already_seen_opaque_enums[tag] = enum
                    self.enums.append(enum)
                    self.all.append(enum)
                    self.output_order.append(('enum', enum))
            else:
                if tag in self.already_seen_opaque_enums:
                    enum = self.already_seen_opaque_enums[tag]
                    enum.opaque = False
                    enum.ctype = ctypeenum
                    enum.src = ctypeenum.src
                    enum.members = ctypeenum.enumerators
                    del self.already_seen_opaque_enums[tag]
                else:
                    enum = EnumDescription((ctypeenum.tag),
                      (ctypeenum.enumerators),
                      src=(
                     filename, str(lineno)),
                      ctype=ctypeenum)
                    enum.opaque = False
                    self.enums.append(enum)
                    self.all.append(enum)
                    self.output_order.append(('enum', enum))
                self.already_seen_enums.add(tag)
                for enumname, expr in ctypeenum.enumerators:
                    constant = ConstantDescription(enumname, expr, src=(filename, lineno))
                    self.constants.append(constant)
                    self.all.append(constant)
                    self.output_order.append(('constant', constant))

    def handle_macro(self, name, params, expr, filename, lineno):
        src = (
         filename, lineno)
        if expr == None:
            expr = ConstantExpressionNode(True)
            constant = ConstantDescription(name, expr, src)
            self.constants.append(constant)
            self.all.append(constant)
            return
        else:
            expr.visit(self)
            if isinstance(expr, CtypesType):
                if params:
                    macro = MacroDescription(name, '', src)
                    macro.error(('%s has parameters but evaluates to a type. Ctypesgen does not support it.' % macro.casual_name()),
                      cls='macro')
                    self.macros.append(macro)
                    self.all.append(macro)
                    self.output_order.append(('macro', macro))
                else:
                    typedef = TypedefDescription(name, expr, src)
                    self.typedefs.append(typedef)
                    self.all.append(typedef)
                    self.output_order.append(('typedef', typedef))
            else:
                if name == '#undef':
                    undef = UndefDescription(expr, src)
                    self.all.append(undef)
                    self.output_order.append(('undef', undef))
                else:
                    macro = MacroDescription(name, params, expr, src)
                    self.macros.append(macro)
                    self.all.append(macro)
                    self.output_order.append(('macro', macro))

    def handle_error(self, message, filename, lineno):
        error_message(('%s:%d: %s' % (filename, lineno, message)), cls='cparser')

    def handle_pp_error(self, message):
        error_message(('%s: %s' % (self.options.cpp, message)), cls='cparser')

    def handle_status(self, message):
        status_message(message)

    def visit_struct(self, struct):
        self.handle_struct(struct, struct.src[0], struct.src[1])

    def visit_enum(self, enum):
        self.handle_enum(enum, enum.src[0], enum.src[1])

    def data(self):
        return DescriptionCollection(self.constants, self.typedefs, self.structs, self.enums, self.functions, self.variables, self.macros, self.all, self.output_order)