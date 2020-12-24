# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_genotype.py
# Compiled at: 2011-11-08 05:15:21
__doc__ = 'Tests for :mod:`cgp.gt.genotype`.'
import numpy as np
from numpy.testing import assert_equal
from nose.tools import raises
from ..gt.genotype import Genotype

def test_genotype_init():
    assert_equal(np.array(Genotype([3, 2])), [
     [
      1, 1],
     [
      1, 0],
     [
      0, 1],
     [
      0, 0],
     [
      2, 1],
     [
      2, 0]])


@raises(AssertionError)
def test_genotype_biallelic():
    Genotype([4, 4])