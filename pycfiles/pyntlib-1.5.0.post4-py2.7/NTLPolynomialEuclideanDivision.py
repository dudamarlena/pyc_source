# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLPolynomialEuclideanDivision.py
# Compiled at: 2018-04-23 08:51:10
import copy
from .NTLUtilities import jsrange
from .NTLValidations import int_check, list_check
__all__ = [
 'polyED', 'polyEDLoop']
nickname = 'polydiv'

def polyED(dvdExp, dvdCoe, dvsExp, dvsCoe):
    list_check(dvdExp, dvdCoe, dvsExp, dvsCoe)
    ecDictDividend = {}
    for ptr in jsrange(len(dvdExp)):
        exp_ = dvdExp[ptr]
        coe_ = dvdCoe[ptr]
        int_check(exp_, coe_)
        ecDictDividend[exp_] = coe_

    ecDictDivisor = {}
    for ptr in jsrange(len(dvsExp)):
        exp_ = dvsExp[ptr]
        coe_ = dvsCoe[ptr]
        int_check(exp_, coe_)
        ecDictDivisor[exp_] = coe_

    ecDictQuotient = {}
    ecDictRemainder = {}
    ecDictQuotient, ecDictRemainder = polyEDLoop(ecDictDividend, ecDictDivisor, ecDictQuotient, ecDictRemainder)
    qttCoe = []
    qttExp = sorted(ecDictQuotient.keys(), reverse=True)
    for exp in qttExp:
        qttCoe.append(ecDictQuotient[exp])

    rmdCoe = []
    rmdExp = sorted(ecDictRemainder.keys(), reverse=True)
    for rmd in rmdExp:
        rmdCoe.append(ecDictRemainder[rmd])

    return (qttExp, qttCoe, rmdExp, rmdCoe)


def polyEDLoop(ecDictDividend, ecDictDivisor, ecDictQuotient, ecDictRemainder):
    ecDDvdCopy = copy.deepcopy(ecDictDividend)
    ecDDvdExpMax = max(ecDictDividend.keys())
    ecDDvsExp = sorted(ecDictDivisor.keys(), reverse=True)
    if ecDictDivisor[ecDDvsExp[0]] != 1:
        flag = True
        ecDDvsCoeMax = ecDictDivisor[ecDDvsExp[0]]
        if ecDictDividend[ecDDvdExpMax] % ecDDvsCoeMax == 0:
            mul_ = ecDictDividend[ecDDvdExpMax] // ecDDvsCoeMax
            for key in ecDictDivisor.keys():
                if ecDictDivisor[key] * mul_ != ecDictDividend[key]:
                    break
            else:
                ecDictQuotient = copy.deepcopy(ecDictDivisor)
                return (ecDictQuotient, ecDictRemainder)

        for exp in ecDDvsExp:
            if ecDictDivisor[exp] % ecDDvsCoeMax != 0:
                ecDictRemainder = copy.deepcopy(ecDictDividend)
                return (
                 ecDictQuotient, ecDictRemainder)
            ecDictDivisor[exp] //= ecDDvsCoeMax

        for key in ecDictDividend.keys():
            if ecDictDividend[key] % ecDDvsCoeMax != 0:
                ecDictRemainder = copy.deepcopy(ecDictDividend)
                return (
                 ecDictQuotient, ecDictRemainder)
            ecDDvdCopy[key] //= ecDDvsCoeMax

    ecDictDividend = copy.deepcopy(ecDDvdCopy)
    while ecDDvdExpMax >= ecDDvsExp[0]:
        ecDQttCoe = ecDictDividend[ecDDvdExpMax]
        ecDQttExp = ecDDvdExpMax - ecDDvsExp[0]
        ecDictQuotient[ecDQttExp] = ecDQttCoe
        for exp in ecDDvsExp:
            tmpexp = exp + ecDQttExp
            if tmpexp in ecDictDividend:
                ecDictDividend[tmpexp] -= ecDictDivisor[exp] * ecDQttCoe
                if ecDictDividend[tmpexp] == 0:
                    ecDictDividend.pop(tmpexp)
            else:
                ecDictDividend[tmpexp] = -1 * ecDictDivisor[exp] * ecDQttCoe

        try:
            ecDDvdExpMax = max(ecDictDividend.keys())
        except ValueError:
            ecDictRemainder = {}
            return (
             ecDictQuotient, ecDictRemainder)

    ecDictRemainder = ecDictDividend.copy()
    return (ecDictQuotient, ecDictRemainder)