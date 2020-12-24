# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpclitools/cli/pdu.py
# Compiled at: 2019-08-11 06:02:11
import sys
from pyasn1.error import PyAsn1Error
from pyasn1.type import univ
from pysnmp import error
from pysnmp.proto import rfc1902
from snmpclitools.cli import base

def getReadUsage():
    return 'Management parameters:\n   [mib-module::]object-name|oid ...\n              mib-module:           MIB name (e.g. SNMPv2-MIB)\n              object-name:          MIB symbol (e.g. sysDescr.0) or OID\n'


class ReadPduScannerMixIn(object):
    __module__ = __name__


class ReadPduParserMixIn(object):
    __module__ = __name__

    def p_varBindSpec(self, args):
        """
        VarBind ::= VarName
        """
        pass

    def p_paramsSpec(self, args):
        """
        Params ::= VarBinds
        """
        pass

    def p_pduSpec(self, args):
        """
        VarBinds ::= VarBind whitespace VarBinds
        VarBinds ::= VarBind
        VarBinds ::=
        VarName ::= ModName semicolon semicolon NodeName
        VarName ::= ModName semicolon semicolon
        VarName ::= semicolon semicolon NodeName
        VarName ::= NodeName
        ModName ::= string
        NodeName ::= ObjectName ObjectIndices
        ObjectName ::= string
        ObjectIndices ::= ObjectIndex string ObjectIndices
        ObjectIndices ::= ObjectIndex ObjectIndices
        ObjectIndices ::= ObjectIndex
        ObjectIndices ::=
        ObjectIndex ::= quote string quote
        """
        pass


class _ReadPduGenerator(base.GeneratorTemplate):
    __module__ = __name__

    def n_ModName(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        ctx['modName'] = node[0].attr

    def n_ObjectName(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        objectName = []
        for subOid in node[0].attr.split('.'):
            if not subOid:
                continue
            try:
                objectName.append(int(subOid))
            except ValueError:
                objectName.append(subOid)

        ctx['objectName'] = tuple(objectName)

    def n_ObjectIndex(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        if 'objectIndices' not in ctx:
            ctx['objectIndices'] = []
        ctx['objectIndices'].append(node[1].attr)

    def n_VarName_exit(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        mibViewCtl = ctx['mibViewController']
        if 'modName' in ctx:
            mibViewCtl.mibBuilder.loadModules(ctx['modName'])
        if 'objectName' in ctx:
            objectName = ctx['objectName']
        else:
            objectName = None
        modName = ctx.get('modName', '')
        if objectName:
            (oid, label, suffix) = mibViewCtl.getNodeName(objectName, modName)
        else:
            (oid, label, suffix) = mibViewCtl.getFirstNodeName(modName)
        if sys.version_info[0] < 3:
            intTypes = (
             int, long)
        else:
            intTypes = (
             int,)
        if [ x for x in suffix if not isinstance(x, intTypes) ]:
            raise error.PySnmpError('Cant resolve object at: %s' % (suffix,))
        (modName, nodeDesc, _suffix) = mibViewCtl.getNodeLocation(oid)
        (mibNode,) = mibViewCtl.mibBuilder.importSymbols(modName, nodeDesc)
        if not hasattr(self, '_MibTableColumn'):
            (self._MibTableColumn,) = mibViewCtl.mibBuilder.importSymbols('SNMPv2-SMI', 'MibTableColumn')
        if isinstance(mibNode, self._MibTableColumn):
            if 'objectIndices' in ctx:
                (modName, nodeDesc, _suffix) = mibViewCtl.getNodeLocation(mibNode.name[:-1])
                (mibNode,) = mibViewCtl.mibBuilder.importSymbols(modName, nodeDesc)
                suffix = suffix + mibNode.getInstIdFromIndices(*ctx['objectIndices'])
        elif 'objectIndices' in ctx:
            raise error.PySnmpError('Cant resolve indices: %s' % (ctx['objectIndices'],))
        ctx['varName'] = oid + suffix
        if 'objectName' in ctx:
            del ctx['objectName']
        if 'objectIndices' in ctx:
            del ctx['objectIndices']
        return

    def n_VarBind_exit(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        if 'varBinds' not in ctx:
            ctx['varBinds'] = [
             (
              ctx['varName'], None)]
        else:
            ctx['varBinds'].append((ctx['varName'], None))
        del ctx['varName']
        return

    def n_VarBinds_exit(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        if 'varBinds' not in ctx or not ctx['varBinds']:
            ctx['varBinds'] = [
             ((1, 3, 6), None)]
        return


def readPduGenerator(cbCtx, ast):
    _ReadPduGenerator().preorder(cbCtx, ast)


def getWriteUsage():
    return 'Management parameters:\n   <[mib-module::]object-name|oid type| = value> ...\n              mib-module:           MIB name (e.g. SNMPv2-MIB)\n              object-name:          MIB symbol (e.g. sysDescr.0) or OID\n              type:                 MIB value type\n                    i               integer\n                    u               unsigned integer\n                    s               string\n                    n               NULL\n                    o               ObjectIdentifier\n                    t               TimeTicks\n                    a               IP address\n              =:                    use MIB for value type lookup\n              value:                value to write\n'


WritePduScannerMixIn = ReadPduScannerMixIn

class WritePduParserMixIn(ReadPduParserMixIn):
    __module__ = __name__

    def p_varBindSpec(self, args):
        """
        VarBind ::= VarName whitespace VarType whitespace VarValue
        VarType ::= string
        VarValue ::= string
        """
        pass


class _WritePduGenerator(_ReadPduGenerator):
    __module__ = __name__
    TYPE_MAP = {'i': rfc1902.Integer(), 'u': rfc1902.Integer32(), 's': rfc1902.OctetString(), 'n': univ.Null(), 'o': univ.ObjectIdentifier(), 't': rfc1902.TimeTicks(), 'a': rfc1902.IpAddress()}

    def n_VarType(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        ctx['varType'] = node[0].attr

    def n_VarValue(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        ctx['varValue'] = node[0].attr

    def n_VarBind_exit(self, cbCtx, node):
        (snmpEngine, ctx) = cbCtx
        mibViewCtl = ctx['mibViewController']
        if ctx['varType'] == '=':
            (modName, nodeDesc, suffix) = mibViewCtl.getNodeLocation(ctx['varName'])
            (mibNode,) = mibViewCtl.mibBuilder.importSymbols(modName, nodeDesc)
            if hasattr(mibNode, 'syntax'):
                (MibTableColumn,) = mibViewCtl.mibBuilder.importSymbols('SNMPv2-SMI', 'MibTableColumn')
                if isinstance(mibNode, MibTableColumn) or suffix == (0, ):
                    val = mibNode.syntax
                else:
                    raise error.PySnmpError('Found MIB scalar %s but non-scalar given %s' % (mibNode.name + (0, ), ctx['varName']))
            else:
                raise error.PySnmpError('Variable %s has no syntax' % (ctx['varName'],))
        else:
            try:
                val = self.TYPE_MAP[ctx['varType']]
            except KeyError:
                raise error.PySnmpError('unsupported SNMP value type "%s"' % ctx['varType'])

            try:
                val = val.clone(ctx['varValue'])
            except PyAsn1Error:
                raise error.PySnmpError(sys.exc_info()[1])

            if 'varBinds' not in ctx:
                ctx['varBinds'] = [
                 (
                  ctx['varName'], val)]
            else:
                ctx['varBinds'].append((ctx['varName'], val))


def writePduGenerator(cbCtx, ast):
    (snmpEngine, ctx) = cbCtx
    _WritePduGenerator().preorder((snmpEngine, ctx), ast)