# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/descriptions.py
# Compiled at: 2019-08-18 21:39:19
"""
ctypesgen.descriptions contains classes to represent a description of a
struct, union, enum, function, constant, variable, or macro. All the
description classes are subclassed from an abstract base class, Description.
The descriptions module also contains a class, DescriptionCollection, to hold
lists of Description objects.
"""

class DescriptionCollection(object):
    """Represents a collection of Descriptions."""

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
    """Represents a constant, typedef, struct, function, variable, enum,
    or macro description. Description is an abstract base class."""

    def __init__(self, src=None):
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
    """Simple class to contain information about a constant."""

    def __init__(self, name, value, src=None):
        Description.__init__(self, src)
        self.name = name
        self.value = value

    def casual_name(self):
        return 'Constant "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.name


class TypedefDescription(Description):
    """Simple container class for a type definition."""

    def __init__(self, name, ctype, src=None):
        Description.__init__(self, src)
        self.name = name
        self.ctype = ctype

    def casual_name(self):
        return 'Typedef "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.name


class StructDescription(Description):
    """Simple container class for a structure or union definition."""

    def __init__(self, tag, packed, variety, members, opaque, ctype, src=None):
        Description.__init__(self, src)
        self.tag = tag
        self.packed = packed
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
    """Simple container class for an enum definition."""

    def __init__(self, tag, members, ctype, src=None):
        Description.__init__(self, src)
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
    """Simple container class for a C function."""

    def __init__(self, name, restype, argtypes, errcheck, variadic=False, src=None):
        Description.__init__(self, src)
        self.name = name
        self.cname = name
        self.restype = restype
        self.argtypes = argtypes
        self.errcheck = errcheck
        self.variadic = variadic

    def casual_name(self):
        return 'Function "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.cname


class VariableDescription(Description):
    """Simple container class for a C variable declaration."""

    def __init__(self, name, ctype, src=None):
        Description.__init__(self, src)
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
    """Simple container class for a C macro."""

    def __init__(self, name, params, expr, src=None):
        Description.__init__(self, src)
        self.name = name
        self.params = params
        self.expr = expr

    def casual_name(self):
        return 'Macro "%s"' % self.name

    def py_name(self):
        return self.name

    def c_name(self):
        return self.name