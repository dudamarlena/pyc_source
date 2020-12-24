# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/entity/rfc3413/mibvar.py
# Compiled at: 2019-08-18 17:24:05
from pyasn1.type import univ
from pysnmp.smi.error import NoSuchObjectError

def mibNameToOid(mibView, name):
    if isinstance(name[0], tuple):
        f = lambda x='', y='': (x, y)
        (modName, symName) = f(*name[0])
        if modName:
            mibView.mibBuilder.loadModules(modName)
        else:
            mibView.mibBuilder.loadModules()
        if symName:
            (oid, label, suffix) = mibView.getNodeNameByDesc(symName, modName)
        else:
            (oid, label, suffix) = mibView.getFirstNodeName(modName)
        suffix = name[1:]
        (modName, symName, _s) = mibView.getNodeLocation(oid)
        (mibNode,) = mibView.mibBuilder.importSymbols(modName, symName)
        if hasattr(mibNode, 'createTest'):
            (modName, symName, _s) = mibView.getNodeLocation(oid[:-1])
            (rowNode,) = mibView.mibBuilder.importSymbols(modName, symName)
            return (
             oid, rowNode.getInstIdFromIndices(*suffix))
        else:
            return (
             oid, suffix)
    elif not isinstance(name, tuple):
        name = tuple(univ.ObjectIdentifier(name))
    (oid, label, suffix) = mibView.getNodeNameByOid(name)
    return (
     oid, suffix)


__scalarSuffix = (
 univ.Integer(0),)

def oidToMibName(mibView, oid):
    if not isinstance(oid, tuple):
        oid = tuple(univ.ObjectIdentifier(oid))
    (_oid, label, suffix) = mibView.getNodeNameByOid(oid)
    (modName, symName, __suffix) = mibView.getNodeLocation(_oid)
    (mibNode,) = mibView.mibBuilder.importSymbols(modName, symName)
    if hasattr(mibNode, 'createTest'):
        (__modName, __symName, __s) = mibView.getNodeLocation(_oid[:-1])
        (rowNode,) = mibView.mibBuilder.importSymbols(__modName, __symName)
        return (
         (
          symName, modName), rowNode.getIndicesFromInstId(suffix))
    elif not suffix:
        return ((symName, modName), suffix)
    elif suffix == (0, ):
        return ((symName, modName), __scalarSuffix)
    else:
        raise NoSuchObjectError(str='No MIB registered that defines %s object, closest known parent is %s (%s::%s)' % (univ.ObjectIdentifier(oid), univ.ObjectIdentifier(mibNode.name), modName, symName))


def cloneFromMibValue(mibView, modName, symName, value):
    (mibNode,) = mibView.mibBuilder.importSymbols(modName, symName)
    if hasattr(mibNode, 'syntax'):
        return mibNode.syntax.clone(value)
    else:
        return