# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/descriptions.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 7836 bytes
__doc__ = '\nctypesgen.descriptions contains classes to represent a description of a\nstruct, union, enum, function, constant, variable, or macro. All the\ndescription classes are subclassed from an abstract base class, Description.\nThe descriptions module also contains a class, DescriptionCollection, to hold\nlists of Description objects.\n'

class DescriptionCollection(object):
    """DescriptionCollection"""

    def __init__(self, constants, typedefs, structs, enums, functions, variables, macros, all, output_order):
        self.constants = constants
        self.typedefs = typedefs
        self.structs = structs
        self.enums = enums
        self.functions = functions
        self.variables = variables
        self.macros = macros
        self.all = all
        self.output_order = output_order


class Description(object):
    """Description"""

    def __init__(self, src=None):
        super(Description, self).__init__()
        self.src = src
        self.include_rule = 'yes'
        self.requirements = set()
        self.dependents = set()
        self.errors = []
        self.warnings = []

    def add_requirements(self, reqs):
        self.requirements = self.requirements.union(reqs)
        for req in reqs:
            req.dependents.add(self)

    def error(self, msg, cls=None):
        self.errors.append((msg, cls))

    def warning(self, msg, cls=None):
        self.warnings.append((msg, cls))

    def __repr__(self):
        return '<Description: %s>' % self.casual_name()

    def casual_name(self):
        """Return a name to show the user."""
        pass

    def py_name(self):
        """Return the name associated with this description in Python code."""
        pass

    def c_name(self):
        """Return the name associated with this description in C code."""
        pass


class ConstantDescription(Description):
    """ConstantDescription"""

    def __init__(self, name, value, src=None):
        super(ConstantDescription, self).__init__(src)
        self.name = name
        self.value = value

    def casual_name(self):
        return 'Constant "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.name


class TypedefDescription(Description):
    """TypedefDescription"""

    def __init__(self, name, ctype, src=None):
        super(TypedefDescription, self).__init__(src)
        self.name = name
        self.ctype = ctype

    def casual_name(self):
        return 'Typedef "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.name


class StructDescription(Description):
    """StructDescription"""

    def __init__(self, tag, attrib, variety, members, opaque, ctype, src=None):
        super(StructDescription, self).__init__(src)
        self.tag = tag
        self.attrib = attrib
        self.variety = variety
        self.members = members
        self.opaque = opaque
        self.ctype = ctype

    def casual_name(self):
        return '%s "%s"' % (self.variety.capitalize(), self.tag)

    def py_name(self):
        return '%s_%s' % (self.variety, self.tag)

    def c_name(self):
        return '%s %s' % (self.variety, self.tag)


class EnumDescription(Description):
    """EnumDescription"""

    def __init__(self, tag, members, ctype, src=None):
        super(EnumDescription, self).__init__(src)
        self.tag = tag
        self.members = members
        self.ctype = ctype

    def casual_name(self):
        return 'Enum "%s"' % self.tag

    def py_name(self):
        return 'enum_%s' % self.tag

    def c_name(self):
        return 'enum %s' % self.tag


class FunctionDescription(Description):
    """FunctionDescription"""

    def __init__(self, name, restype, argtypes, errcheck, variadic, attrib, src):
        super(FunctionDescription, self).__init__(src)
        self.name = name
        self.cname = name
        self.restype = restype
        self.argtypes = argtypes
        self.errcheck = errcheck
        self.variadic = variadic
        self.attrib = attrib

    def casual_name(self):
        return 'Function "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.cname


class VariableDescription(Description):
    """VariableDescription"""

    def __init__(self, name, ctype, src=None):
        super(VariableDescription, self).__init__(src)
        self.name = name
        self.cname = name
        self.ctype = ctype

    def casual_name(self):
        return 'Variable "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.cname


class MacroDescription(Description):
    """MacroDescription"""

    def __init__(self, name, params, expr, src=None):
        super(MacroDescription, self).__init__(src)
        self.name = name
        self.params = params
        self.expr = expr

    def casual_name(self):
        return 'Macro "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.name


class UndefDescription(Description):
    """UndefDescription"""

    def __init__(self, macro, src=None):
        super(UndefDescription, self).__init__(src)
        self.include_rule = 'if_needed'
        self.macro = macro

    def casual_name(self):
        return 'Undef "%s"' % self.macro.name

    def py_name(self):
        return '#undef:%s' % self.macro.name

    def c_name(self):
        return '#undef %s' % self.macro.name