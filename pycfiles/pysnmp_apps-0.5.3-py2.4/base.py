# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_apps/cli/base.py
# Compiled at: 2018-01-07 03:15:27
import sys
from pysnmp_apps.cli import spark

class ConfigToken:
    __module__ = __name__

    def __init__(self, typ, attr=None):
        self.type = typ
        self.attr = attr

    def __eq__(self, other):
        return self.type == other

    def __ne__(self, other):
        return self.type != other

    def __lt__(self, other):
        return self.type < other

    def __le__(self, other):
        return self.type <= other

    def __gt__(self, other):
        return self.type > other

    def __ge__(self, other):
        return self.type >= other

    def __repr__(self):
        return self.attr or self.type

    def __str__(self):
        if self.attr is None:
            return '%s' % self.type
        else:
            return '%s(%s)' % (self.type, self.attr)
        return


class ConfigNode:
    __module__ = __name__

    def __init__(self, typ, attr=None):
        self.type, self.attr = typ, attr
        self._kids = []

    def __getitem__(self, i):
        return self._kids[i]

    def __len__(self):
        return len(self._kids)

    if sys.version_info[0] < 3:

        def __setslice__(self, low, high, seq):
            self._kids[low:high] = seq

    else:

        def __setitem__(self, idx, seq):
            self._kids[idx] = seq

    def __eq__(self, other):
        return self.type == other

    def __ne__(self, other):
        return self.type != other

    def __lt__(self, other):
        return self.type < other

    def __le__(self, other):
        return self.type <= other

    def __gt__(self, other):
        return self.type > other

    def __ge__(self, other):
        return self.type >= other

    def __str__(self):
        if self.attr is None:
            return self.type
        else:
            return '%s(%s)' % (self.type, self.attr)
        return


class __ScannerTemplate(spark.GenericScanner):
    __module__ = __name__

    def tokenize(self, data):
        self.rv = []
        spark.GenericScanner.tokenize(self, data)
        return self.rv


class __FirstLevelScanner(__ScannerTemplate):
    __module__ = __name__

    def t_string(self, s):
        r""" [!#\$%&\'\(\)\*\+,\.//0-9<=>\?@A-Z\\\^_`a-z\{\|\}~][!#\$%&\'\(\)\*\+,\-\.//0-9<=>\?@A-Z\\\^_`a-z\{\|\}~]* """
        self.rv.append(ConfigToken('string', s))


class __SecondLevelScanner(__FirstLevelScanner):
    __module__ = __name__

    def t_semicolon(self, s):
        """ : """
        self.rv.append(ConfigToken('semicolon'))

    def t_lparen(self, s):
        r""" \[ """
        self.rv.append(ConfigToken('lparen'))

    def t_rparen(self, s):
        r""" \] """
        self.rv.append(ConfigToken('rparen'))

    def t_quote(self, s):
        r""" \" """
        self.rv.append(ConfigToken('quote'))

    def t_whitespace(self, s):
        r""" \s+ """
        self.rv.append(ConfigToken('whitespace'))


ScannerTemplate = __SecondLevelScanner

class ParserTemplate(spark.GenericASTBuilder):
    __module__ = __name__
    initialSymbol = None

    def __init__(self, startSymbol=None):
        if startSymbol is None:
            startSymbol = self.initialSymbol
        spark.GenericASTBuilder.__init__(self, ConfigNode, startSymbol)
        return

    def terminal(self, token):
        return ConfigNode(token.type, token.attr)


class GeneratorTemplate(spark.GenericASTTraversal):
    __module__ = __name__

    def __init__(self):
        pass

    def typestring(self, node):
        return node.type

    def preorder(self, client, node):
        try:
            name = 'n_' + self.typestring(node)
            if hasattr(self, name):
                func = getattr(self, name)
                func(client, node)
            else:
                self.default(client, node)
        except spark.GenericASTTraversalPruningException:
            return client

        for kid in node:
            self.preorder(client, kid)

        name = name + '_exit'
        if hasattr(self, name):
            func = getattr(self, name)
            func(client, node)
        return client

    def default(self, client, node):
        pass