# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_vma_ra_enabled_s390x.py
# Compiled at: 2019-12-13 11:35:35
from insights.parsers import SkipException
from insights.tests import context_wrap
from insights.parsers import vma_ra_enabled_s390x
from insights.parsers.vma_ra_enabled_s390x import VmaRaEnabledS390x
import pytest, doctest
INPUT_VMA_1 = ('\nTrue\n').strip()
INPUT_VMA_2 = ('\nFalse\n').strip()

def test_vma_ra_enabled_s390x():
    sp1 = VmaRaEnabledS390x(context_wrap(INPUT_VMA_1))
    sp2 = VmaRaEnabledS390x(context_wrap(INPUT_VMA_2))
    assert sp1.ra_enabled is True
    assert sp2.ra_enabled is False


def test_vma_ra_enabled_s390x_exp():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc1):
        VmaRaEnabledS390x(context_wrap(''))
    assert 'Input content is empty' in str(sc1)


def test_vma_ra_enabled_s390x__documentation():
    """
    Here we test the examples in the documentation automatically using doctest.
    We set up an environment which is similar to what a rule writer might see -
    a '/sys/kernel/mm/swap/vma_ra_enabled' output that has been passed in as a
    parameter to the rule declaration.
    """
    env = {'vma': VmaRaEnabledS390x(context_wrap(INPUT_VMA_1))}
    failed, total = doctest.testmod(vma_ra_enabled_s390x, globs=env)
    assert failed == 0