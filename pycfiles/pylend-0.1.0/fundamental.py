# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/model/fundamental.py
# Compiled at: 2016-07-11 11:37:55
__doc__ = '\nDimension and Unit definitions in terms of the fundamental SI units.\n\n@author: Gautham Ganapathy\n@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)\n@contact: gautham@lisphacker.org\n'
from lems.base.base import LEMSBase

class Include(LEMSBase):
    """
    Include another LEMS file.
    """

    def __init__(self, filename):
        """
        Constructor.

        @param filename: Name of the file.
        @type name: str

        """
        self.file = filename

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return '<Include file="%s"/>' % self.file


class Dimension(LEMSBase):
    """
    Stores a dimension in terms of the seven fundamental SI units.
    """

    def __init__(self, name, description='', **params):
        """
        Constructor.

        @param name: Name of the dimension.
        @type name: str

        @param params: Key arguments specifying powers for each of the 
        seven fundamental SI dimensions.
        @type params: dict()
        """
        self.name = name
        self.m = params['m'] if 'm' in params else 0
        self.l = params['l'] if 'l' in params else 0
        self.t = params['t'] if 't' in params else 0
        self.i = params['i'] if 'i' in params else 0
        self.k = params['k'] if 'k' in params else 0
        self.n = params['n'] if 'n' in params else 0
        self.j = params['j'] if 'j' in params else 0
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Dimension name="{0}"').format(self.name) + ((' m = "{0}"').format(self.m) if self.m != 0 else '') + ((' l = "{0}"').format(self.l) if self.l != 0 else '') + ((' t = "{0}"').format(self.t) if self.t != 0 else '') + ((' i = "{0}"').format(self.i) if self.i != 0 else '') + ((' k = "{0}"').format(self.k) if self.k != 0 else '') + ((' n = "{0}"').format(self.n) if self.n != 0 else '') + ((' j = "{0}"').format(self.j) if self.j != 0 else '') + '/>'


class Unit(LEMSBase):
    """
    Stores a unit definition.
    """

    def __init__(self, name, symbol, dimension, power=0, scale=1.0, offset=0.0, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.symbol = symbol
        self.dimension = dimension
        self.power = power
        self.scale = scale
        self.offset = offset
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return '<Unit' + ((' symbol = "{0}"').format(self.symbol) if self.symbol else '') + ((' dimension = "{0}"').format(self.dimension) if self.dimension else '') + ((' power = "{0}"').format(self.power) if self.power else '') + ((' scale = "{0}"').format(self.scale) if self.scale else '') + ((' offset = "{0}"').format(self.offset) if self.offset else '') + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'