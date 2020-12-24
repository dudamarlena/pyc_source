# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_genotype.py
# Compiled at: 2011-11-08 05:15:21
"""Tests for :mod:`cgp.gt.genotype`."""
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