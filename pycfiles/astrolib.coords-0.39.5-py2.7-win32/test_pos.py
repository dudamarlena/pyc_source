# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\astrolib\coords\tests\test_pos.py
# Compiled at: 2014-01-13 11:58:06
import astrolib.coords.position as P

class Tvalues:

    def __init__(self):
        self.epsilon = 1e-06
        self.hms_zero = '00:00:00.000 +00:00:00.000'
        self.dd_zero = (0.0, 0.0)
        self.rad_zero = (0.0, 0.0)
        self.hms_posarb = '01:23:45.300 +65:43:31.240'
        self.dd_posarb = (20.93875, 65.725344444444)
        self.rad_posarb = (0.3654501287519627, 1.147123662562911)
        self.hms_negarb = '18:53:23.541 -33:44:17.123'
        self.dd_negarb = (283.3480875, -33.738089722222)
        self.rad_negarb = (4.945357056103989, -0.588840748986033)
        self.detail_string = ' System: celestial \n Equinox: j2000 '


std_eps = Tvalues()

def fuzzy_equal(a, b, epsilon):
    diff = abs(a - b)
    return diff <= epsilon


def fuzzy_tuple(a, b, epsilon):
    result = True
    for i in range(len(a)):
        result = result and fuzzy_equal(a[i], b[i], epsilon)

    return result


def test_zero_hms():
    t = std_eps
    p = P.Position(t.hms_zero)
    res = p.dd()
    assert res == t.dd_zero, 'Fail: result = ' + `res`


def test_zero_dd():
    t = std_eps
    p = P.Position(t.dd_zero)
    res = p.hmsdms()
    assert res == t.hms_zero, 'Fail: result = ' + res


def test_zero_rad():
    t = std_eps
    p = P.Position(t.rad_zero, units='rad')
    res = p.dd()
    assert res == t.dd_zero, 'Fail: result = (%f,%f)' % res


def test_posarb_hms():
    t = std_eps
    p = P.Position(t.hms_posarb)
    res = p.dd()
    assert fuzzy_tuple(res, t.dd_posarb, t.epsilon), 'Fail: result = ' + `res`


def test_posarb_dd():
    t = std_eps
    p = P.Position(t.dd_posarb)
    res = p.hmsdms()
    assert res == t.hms_posarb, 'Fail: result = ' + res


def test_posarb_rad():
    t = std_eps
    p = P.Position(t.rad_posarb, units='rad')
    res = p.dd()
    assert fuzzy_tuple(res, t.dd_posarb, t.epsilon), 'Fail: result = (%f,%f)' % res


def test_negarb_hms():
    t = std_eps
    p = P.Position(t.hms_negarb)
    res = p.dd()
    assert fuzzy_tuple(res, t.dd_negarb, t.epsilon), 'Fail: result = ' + `res`


def test_negarb_dd():
    t = std_eps
    p = P.Position(t.dd_negarb)
    res = p.hmsdms()
    assert res == t.hms_negarb, 'Fail: result = ' + res


def test_negarb_rad():
    t = std_eps
    p = P.Position(t.rad_negarb, units='rad')
    res = p.dd()
    assert fuzzy_tuple(res, t.dd_negarb, t.epsilon), 'Fail: result = (%f,%f)' % res


def test_details():
    t = std_eps
    p = P.Position(t.dd_posarb)
    res = p.details()
    assert res == t.detail_string, 'Fail: result = \n' + res


def test_angsep1():
    t = std_eps
    p1 = P.Position(t.dd_posarb)
    sep = p1.angsep(p1)
    assert sep._internal == 0.0, 'Fail angsep1: result=%f' % sep._internal


def test_angsep2():
    t = std_eps
    p1 = P.Position((t.dd_posarb[0], 0.0))
    p2 = P.Position((t.dd_posarb[0] + 2.5, 0.0))
    sep = p1.angsep(p2)
    assert fuzzy_equal(sep._internal, 2.5, 1e-07), 'Fail angsep2: abs(sep-2.5) > 0.0000001)'


def test_angsep3():
    t = std_eps
    p1 = P.Position(t.dd_posarb)
    p2 = P.Position(t.dd_negarb)
    sep = p1.angsep(p2)
    sep.setunits('rad')
    assert fuzzy_equal(sep.value, 2.1548999, 1e-07), 'Fail angsep3: %f, %f' % (sep.value, 2.1548999)


def test_within1():
    t = std_eps
    p1 = P.Position(t.dd_posarb)
    p2 = P.Position((t.dd_posarb[0], t.dd_posarb[1] + 0.24))
    ans = p1.within(p2, 0.3, units='degrees')
    assert ans, 'Fail within1'


def test_within2():
    t = std_eps
    p1 = P.Position(t.dd_posarb)
    p2 = P.Position((t.dd_posarb[0], t.dd_posarb[1] + 0.24))
    ans = p1.within(p2, 0.3, units='arcsec')
    assert not ans, 'Fail within2'


def test_within3():
    t = std_eps
    p1 = P.Position(t.dd_posarb)
    ans = p1.within(p1, 0.2)
    assert ans, 'Fail within3'


def test_negdeg():
    t = std_eps
    p1 = P.Position('1:2:3 -0:32:22.3')
    dd = p1.dd()
    assert dd[(-1)] < 0, 'Fail negdeg'


def test_negmin():
    t = std_eps
    p1 = P.Position('1:2:3 -0:0:22.3')
    dd = p1.dd()
    assert dd[(-1)] < 0, 'Fail negmin'


def run():
    test_zero_hms()
    test_zero_dd()
    test_zero_rad()
    test_posarb_hms()
    test_posarb_dd()
    test_posarb_rad()
    test_negarb_hms()
    test_negarb_dd()
    test_negarb_rad()
    test_details()
    test_angsep1()
    test_angsep2()
    test_angsep3()
    test_within1()
    test_within2()
    test_within3()
    test_negdeg()
    test_negmin()