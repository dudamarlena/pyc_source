# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\capitalControlbylw.py
# Compiled at: 2019-06-05 03:26:03
# Size of source mod 2**32: 1197 bytes
"""
Created on Thu Sep 27 14:39:54 2018
资金管理
@author: SH
"""
from pyalgotrade import commonHelpBylw
fenshu = 3

def fixedShares4wangzong():
    sharesDict = {}
    sharesDict['SHFE.RB'] = 25
    sharesDict['SHFE.NI'] = 10
    sharesDict['SHFE.CU'] = 4
    sharesDict['DCE.J'] = 4
    sharesDict['SHFE.BU'] = 25
    sharesDict['CZCE.MA'] = 30
    sharesDict['DCE.PP'] = 20
    sharesDict['DCE.P'] = 20
    sharesDict['CZCE.SM'] = 25
    sharesDict['CFFEX.T'] = 1
    sharesDict['CZCE.SR'] = 20
    sharesDict['CZCE.CF'] = 15
    return sharesDict


def getVolofwangzong(aSymbol):
    sharesDict = {}
    sharesDict['SHFE.RB'] = 25
    sharesDict['SHFE.NI'] = 10
    sharesDict['SHFE.CU'] = 4
    sharesDict['DCE.J'] = 4
    sharesDict['SHFE.BU'] = 25
    sharesDict['CZCE.MA'] = 30
    sharesDict['DCE.PP'] = 20
    sharesDict['DCE.P'] = 20
    sharesDict['CZCE.SM'] = 25
    sharesDict['CFFEX.T'] = 1
    sharesDict['CZCE.SR'] = 20
    sharesDict['CZCE.CF'] = 15
    mainContract = commonHelpBylw.getMainContinContract(aSymbol)
    vol = sharesDict[mainContract]
    return vol