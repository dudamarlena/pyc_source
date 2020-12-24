# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/constants/tests/test_xrf.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 7083 bytes
from __future__ import absolute_import, division, print_function
import six
from numpy.testing import assert_array_equal, assert_raises
from nose.tools import assert_equal, assert_not_equal
from skxray.core.constants.xrf import XrfElement, emission_line_search, XrayLibWrap, XrayLibWrap_Energy
from skxray.core.utils import NotInstalledError
from skxray.core.constants.basic import basic

def test_element_data():
    """
    smoke test of all elements
    """
    data1 = []
    data2 = []
    name_list = []
    for i in range(100):
        e = XrfElement(i + 1)
        data1.append(e.cs(10)['Ka1'])
        name_list.append(e.name)

    for item in name_list:
        e = XrfElement(item)
        data2.append(e.cs(10)['Ka1'])

    assert_array_equal(data1, data2)


def test_element_finder():
    true_name = sorted(['Eu', 'Cu'])
    out = emission_line_search(8, 0.05, 10)
    found_name = sorted(list(six.iterkeys(out)))
    assert_equal(true_name, found_name)


def test_XrayLibWrap_notpresent():
    from skxray.core.constants import xrf
    xraylib = xrf.xraylib
    xrf.xraylib = None
    assert_raises(NotInstalledError, xrf.XrfElement, None)
    assert_raises(NotInstalledError, xrf.emission_line_search, None, None, None)
    assert_raises(NotInstalledError, xrf.XrayLibWrap, None, None)
    assert_raises(NotInstalledError, xrf.XrayLibWrap_Energy, None, None, None)
    xrf.xraylib = xraylib


def test_XrayLibWrap():
    for Z in range(1, 101):
        for infotype in XrayLibWrap.opts_info_type:
            xlw = XrayLibWrap(Z, infotype)
            assert_not_equal(xlw.all, None)
            for key in xlw:
                assert_not_equal(xlw[key], None)

            assert_equal(xlw.info_type, infotype)
            len(xlw)


def test_XrayLibWrap_Energy():
    for Z in range(1, 101):
        for infotype in XrayLibWrap_Energy.opts_info_type:
            incident_energy = 10
            xlwe = XrayLibWrap_Energy(element=Z, info_type=infotype, incident_energy=incident_energy)
            incident_energy *= 2
            xlwe.incident_energy = incident_energy
            assert_equal(xlwe.incident_energy, incident_energy)
            assert_equal(xlwe.info_type, infotype)


def smoke_test_element_creation():
    prev_element = None
    elements = [elm for abbrev, elm in six.iteritems(basic) if isinstance(abbrev, int)]
    elements.sort()
    for element in elements:
        Z = element.Z
        mass = element.mass
        density = element.density
        sym = element.sym
        inits = [Z, sym, sym.upper(), sym.lower(), sym.swapcase()]
        element = None
        for init in inits:
            element = XrfElement(init)
            element.bind_energy
            element.fluor_yield
            element.jump_factor
            element.emission_line.all
            if prev_element is not None:
                assert_equal(prev_element.__lt__(element), True)
                assert_equal(prev_element < element, True)
                assert_equal(prev_element.__eq__(element), False)
                assert_equal(prev_element == element, False)
                assert_equal(prev_element >= element, False)
                assert_equal(prev_element > element, False)
                assert_equal(element < prev_element, False)
                assert_equal(element.__lt__(prev_element), False)
                assert_equal(element <= prev_element, False)
                assert_equal(element.__eq__(prev_element), False)
                assert_equal(element == prev_element, False)
                assert_equal(element >= prev_element, True)
                assert_equal(element > prev_element, True)

        prev_element = element


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)