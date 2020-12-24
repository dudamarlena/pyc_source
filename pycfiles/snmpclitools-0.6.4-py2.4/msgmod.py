# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpclitools/cli/msgmod.py
# Compiled at: 2019-08-11 06:02:11
from pysnmp import error
from snmpclitools.cli import base

def getUsage():
    return 'SNMP message processing options:\n   -v VERSION            SNMP version (1|2c|3)\n'


class MPScannerMixIn(object):
    __module__ = __name__

    def t_version(self, s):
        """ -v """
        self.rv.append(base.ConfigToken('version'))


class MPParserMixIn(object):
    __module__ = __name__

    def p_mpSpec(self, args):
        """
        Option ::= SnmpVersionId
        SnmpVersionId ::= version string
        SnmpVersionId ::= version whitespace string
        """
        pass


class _MPGenerator(base.GeneratorTemplate):
    __module__ = __name__
    VERSION_ID_MAP = {'1': 0, '2': 1, '2c': 1, '3': 3}

    def n_SnmpVersionId(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        if len(node) > 2:
            versionId = node[2].attr
        else:
            versionId = node[1].attr
        if versionId in self.VERSION_ID_MAP:
            ctx['versionId'] = self.VERSION_ID_MAP[versionId]
        else:
            raise error.PySnmpError('Bad version value %s' % versionId)


def generator(cbCtx, ast):
    (snmpEngine, ctx) = cbCtx
    _MPGenerator().preorder((snmpEngine, ctx), ast)
    if 'versionId' not in ctx:
        ctx['versionId'] = 3