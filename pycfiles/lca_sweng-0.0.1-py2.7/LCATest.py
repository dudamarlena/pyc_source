# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lca_sweng\LCATest.py
# Compiled at: 2019-10-16 07:17:06
from LCAImplementation import *
import pytest

def testEmptySize():
    newTree = LCA()
    assert newTree.__size__() is 0


def testEmptySizeB():
    newTree = LCA()
    assert newTree.isempty() is True


def testSmallTree():
    newTreeA = LCA()
    newTreeA.insert(4)
    newTreeA.insert(6)
    newTreeA.insert(-2)
    newTreeA.insert(7)
    newTreeA.insert(8)
    newTreeA.insert(9)
    assert newTreeA.isempty() is False


def testSmallTreeB():
    newTreeA = LCA()
    newTreeA.insert(4)
    newTreeA.insert(6)
    newTreeA.insert(-2)
    newTreeA.insert(7)
    newTreeA.insert(8)
    newTreeA.insert(9)
    assert newTreeA.__size__() is 6


def testRepeatTree():
    newTreeB = LCA()
    newTreeB.insert(55)
    newTreeB.insert(55)
    newTreeB.insert(2)
    newTreeB.insert(-71)
    newTreeB.insert(71)
    newTreeB.insert(967)
    newTreeB.insert(67)
    assert newTreeB.isempty() is False


def testRepeatTreeB():
    newTreeB = LCA()
    newTreeB.insert(55)
    newTreeB.insert(55)
    newTreeB.insert(2)
    newTreeB.insert(-71)
    newTreeB.insert(71)
    newTreeB.insert(967)
    newTreeB.insert(67)
    assert newTreeB.__size__() is 6


def testNonIntTree():
    newTreeC = LCA()
    newTreeC.insert('hi')
    newTreeC.insert('sharon')
    newTreeC.insert(2)
    newTreeC.insert(71)
    newTreeC.insert(7)
    newTreeC.insert(97)
    newTreeC.insert('sweng')
    newTreeC.insert(27)
    newTreeC.insert(-100)
    newTreeC.insert(87)
    assert newTreeC.isempty() is False


def testNonIntTreeB():
    newTreeC = LCA()
    newTreeC.insert('hi')
    newTreeC.insert('sharon')
    newTreeC.insert(2)
    newTreeC.insert(71)
    newTreeC.insert(7)
    newTreeC.insert(97)
    newTreeC.insert('sweng')
    newTreeC.insert(27)
    newTreeC.insert(-100)
    newTreeC.insert(87)
    assert newTreeC.__size__() is 7


def teststringTree():
    newTreeD = LCA()
    newTreeD.insert('sharon')
    newTreeD.insert('loves')
    newTreeD.insert('SWENG')
    assert newTreeD.isempty() is True


def teststringTreeB():
    newTreeD = LCA()
    newTreeD.insert('sharon')
    newTreeD.insert('loves')
    newTreeD.insert('SWENG')
    assert newTreeD.__size__() is 0


def testemptyLCA():
    newTreeE = LCA()
    assert newTreeE.findlca(14, 50) is False


def testSmallLCA():
    newTreeF = LCA()
    newTreeF.insert(4)
    newTreeF.insert(6)
    newTreeF.insert(-2)
    newTreeF.insert(7)
    assert newTreeF.findlca(4, -2) is 4


def testLargeLCA():
    newTreeG = LCA()
    newTreeG.insert(4)
    newTreeG.insert(6)
    newTreeG.insert(-2)
    newTreeG.insert(27)
    newTreeG.insert(47)
    newTreeG.insert(61)
    newTreeG.insert(-23)
    newTreeG.insert(97)
    newTreeG.insert(433)
    newTreeG.insert(67)
    newTreeG.insert(-92)
    newTreeG.insert(374)
    newTreeG.insert(14)
    newTreeG.insert(623)
    newTreeG.insert(-42)
    newTreeG.insert(17)
    newTreeG.insert(400)
    newTreeG.insert(621)
    newTreeG.insert(-62)
    newTreeG.insert(37)
    assert newTreeG.findlca(374, 67) is 97


def testMissingLCA():
    newTreeH = LCA()
    newTreeH.insert(4)
    newTreeH.insert(6)
    newTreeH.insert(-2)
    newTreeH.insert(27)
    newTreeH.insert(47)
    newTreeH.insert(61)
    assert newTreeH.findlca(6, 67) is -1


def testStringTreeLCA():
    newTreeI = LCA()
    newTreeI.insert(4)
    newTreeI.insert(6)
    newTreeI.insert('string')
    newTreeI.insert(27)
    newTreeI.insert(47)
    newTreeI.insert('sharon')
    assert newTreeI.findlca(6, 67) is -1


def testStringSearchTreeLCA():
    newTreeI = LCA()
    newTreeI.insert(4)
    newTreeI.insert(6)
    newTreeI.insert('string')
    newTreeI.insert(27)
    newTreeI.insert(47)
    newTreeI.insert('sharon')
    assert newTreeI.findlca('string', 67) is False