# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./URI.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 4733 bytes
import types, string, re, CosNaming
from omniORB import CORBA
__regex = re.compile('([/\\.\\\\])')

def stringToName(sname):
    """stringToName(string) -> CosNaming.Name

Convert a stringified name to a CosNaming.Name"""
    if not isinstance(sname, str):
        raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_WrongPythonType, COMPLETED_NO)
    if sname == '':
        raise CosNaming.NamingContext.InvalidName()
    parts = __regex.split(sname)
    name = [CosNaming.NameComponent('', '')]
    dotseen = 0
    parts = [_f for _f in parts if _f]
    parts.reverse()
    while parts:
        part = parts.pop()
        if part == '\\':
            if not parts:
                raise CosNaming.NamingContext.InvalidName()
            part = parts.pop()
            if part != '\\':
                if part != '/':
                    if part != '.':
                        raise CosNaming.NamingContext.InvalidName()
        else:
            if part == '.':
                if dotseen:
                    raise CosNaming.NamingContext.InvalidName()
                dotseen = 1
                continue
            else:
                if part == '/':
                    if not parts:
                        raise CosNaming.NamingContext.InvalidName()
                    if dotseen:
                        if name[(-1)].kind == '':
                            if name[(-1)].id != '':
                                raise CosNaming.NamingContext.InvalidName()
                    else:
                        if name[(-1)].id == '':
                            raise CosNaming.NamingContext.InvalidName()
                        dotseen = 0
                        name.append(CosNaming.NameComponent('', ''))
                        continue
        if dotseen:
            name[(-1)].kind = name[(-1)].kind + part
        else:
            name[(-1)].id = name[(-1)].id + part

    return name


def nameToString(name):
    """nameToString(CosNaming.Name) -> string

Convert the CosNaming.Name into its stringified form."""
    parts = []
    if not isinstance(name, (list, tuple)):
        raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_WrongPythonType, COMPLETED_NO)
    if len(name) == 0:
        raise CosNaming.NamingContext.InvalidName()
    try:
        for nc in name:
            if nc.id == '' and nc.kind == '':
                parts.append('.')
            else:
                if nc.kind == '':
                    parts.append(__regex.sub('\\\\\\1', nc.id))
                else:
                    parts.append(__regex.sub('\\\\\\1', nc.id) + '.' + __regex.sub('\\\\\\1', nc.kind))

    except AttributeError:
        raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_WrongPythonType, COMPLETED_NO)

    return '/'.join(parts)


def addrAndNameToURI(addr, sname):
    """addrAndNameToURI(addr, sname) -> URI

Create a valid corbaname URI from an address string and a stringified name"""
    import urllib.request, urllib.parse, urllib.error
    if not (isinstance(addr, str) and isinstance(sname, str)):
        raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_WrongPythonType, COMPLETED_NO)
    if addr == '':
        raise CosNaming.NamingContextExt.InvalidAddress()
    if sname == '':
        return 'corbaname:' + addr
    else:
        stringToName(sname)
        return 'corbaname:' + addr + '#' + urllib.parse.quote(sname)