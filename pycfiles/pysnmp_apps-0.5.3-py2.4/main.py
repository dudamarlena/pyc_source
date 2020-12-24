# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_apps/cli/main.py
# Compiled at: 2018-01-07 03:15:27
import sys
from pysnmp.smi import view
from pysnmp_apps.cli import base
from pysnmp import error
from pysnmp_apps import __version__ as pysnmpAppsVersion
try:
    from pysnmp import __version__ as pysnmpVersion
except ImportError:
    pysnmpVersion = 'N/A'

try:
    from pysmi import __version__ as pysmiVersion
except ImportError:
    pysmiVersion = 'N/A'

try:
    from pyasn1 import __version__ as pyasn1Version
except ImportError:
    pyasn1Version = 'N/A'

try:
    from pysnmp import debug
except ImportError:
    debug = None

def getUsage():
    return 'Command-line SNMP tools version %s, written by Ilya Etingof <etingof@gmail.com>\nFoundation libraries: pysmi %s, pysnmp %s, pyasn1 %s\nPython interpreter: %s\nSoftware documentation and support at http://snmplabs.com\n   -h                    display this help message\n   -V                    software release information\n   -d                    dump raw packets\n   -D category           enable debugging [%s]\n' % (pysnmpAppsVersion, pysmiVersion, pysnmpVersion, pyasn1Version, sys.version.replace('\n', ''), debug and (',').join(debug.flagMap.keys()) or '')


class MainScannerMixIn:
    __module__ = __name__

    def t_help(self, s):
        """ -h|--help """
        self.rv.append(base.ConfigToken('help'))

    def t_versioninfo(self, s):
        """ -V|--version """
        self.rv.append(base.ConfigToken('versioninfo'))

    def t_dump(self, s):
        """ -d """
        self.rv.append(base.ConfigToken('dump'))

    def t_debug(self, s):
        """ -D|--debug """
        self.rv.append(base.ConfigToken('debug'))


class MainParserMixIn:
    __module__ = __name__
    initialSymbol = 'Cmdline'

    def error(self, token):
        raise error.PySnmpError('Command-line parser error at token %s\n' % token)

    def p_cmdline(self, args):
        """
        Cmdline ::= Options Agent whitespace Params
        """
        pass

    def p_cmdlineExt(self, args):
        """
        Options ::= Option whitespace Options
        Options ::= Option
        Options ::=

        Option ::= Help
        Option ::= VersionInfo
        Option ::= DebugOption

        Help ::= help

        VersionInfo ::= versioninfo

        DebugOption ::= Dump
        DebugOption ::= Debug
        Dump ::= dump
        Debug ::= debug string
        Debug ::= debug whitespace string
        """
        pass


class __MainGenerator(base.GeneratorTemplate):
    __module__ = __name__

    def n_VersionInfo(self, cbCtx, node):
        raise error.PySnmpError()

    def n_Help(self, cbCtx, node):
        raise error.PySnmpError()

    def n_Dump(self, cbCtx, node):
        if debug:
            debug.setLogger(debug.Debug('io'))

    def n_Debug(self, cbCtx, node):
        if debug:
            if len(node) > 2:
                f = node[2].attr
            else:
                f = node[1].attr
            debug.setLogger(debug.Debug(*f.split(',')))


def generator(cbCtx, ast):
    (snmpEngine, ctx) = cbCtx
    ctx['mibViewController'] = view.MibViewController(snmpEngine.getMibBuilder())
    return __MainGenerator().preorder((snmpEngine, ctx), ast)