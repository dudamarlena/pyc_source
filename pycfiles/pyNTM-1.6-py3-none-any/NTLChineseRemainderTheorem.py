# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLChineseRemainderTheorem.py
# Compiled at: 2018-04-23 08:51:10
from .NTLBezoutEquation import bezoutEquation
from .NTLExceptions import DefinitionError
from .NTLUtilities import jsrange
from .NTLValidations import int_check, list_check, tuple_check
__all__ = [
 'CHNRemainderTheorem', 'solve', 'iterCalc', 'updateState']
nickname = 'crt'

def CHNRemainderTheorem(*args):
    rmd = []
    mod = []
    for tpl in args:
        tuple_check(tpl)
        if len(tpl) != 2:
            raise DefinitionError('The arguments must be tuples of modulos and corresponding solutions (in a list).')
        int_check(tpl[0])
        list_check(tpl[1])
        for num in tpl[1]:
            int_check(num)

        mod.append(tpl[0])
        rmd.append(tpl[1])

    modulo = 1
    for tmpMod1 in mod:
        modulo *= tmpMod1

    bList = []
    for tmpMod in mod:
        M = modulo // tmpMod
        t = bezoutEquation(M, tmpMod)[0]
        bList.append(t * M)

    remainder = iterCalc(rmd, bList, modulo)
    return sorted(remainder)


def iterCalc(ognList, coeList, modulo):
    ptrList = []
    lvlList = []
    for tmpList in ognList:
        ptrList.append(len(tmpList) - 1)
        lvlList.append(len(tmpList) - 1)

    flag = 1
    rstList = []
    while flag:
        ptrNum = 0
        rstNum = 0
        for ptr in ptrList:
            rstNum += ognList[ptrNum][ptr] * coeList[ptrNum]
            ptrNum += 1

        rstList.append(rstNum % modulo)
        ptrList, flag = updateState(ptrList, lvlList)

    return rstList


def updateState(ptrList, lvlList):
    ptr = 0
    flag = 1
    glbFlag = 1
    while flag:
        if ptrList[ptr] > 0:
            ptrList[ptr] -= 1
            flag = 0
        elif ptr < len(lvlList) - 1:
            ptrList[ptr] = lvlList[ptr]
            ptr += 1
        else:
            flag = 0
            glbFlag = 0

    return (ptrList, glbFlag)