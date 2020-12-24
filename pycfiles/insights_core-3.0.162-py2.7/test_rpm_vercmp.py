# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rpm_vercmp.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers.rpm_vercmp import _rpm_vercmp
DEFAULT_DATA = '\nm4_define([RPMVERCMP],[\nAT_SETUP([rpmvercmp($1, $2) = $3])\nAT_KEYWORDS([vercmp])\nAT_CHECK([\nAT_SKIP_IF([$LUA_DISABLED])\nrunroot rpm --eval \'%{lua: print(rpm.vercmp("$1", "$2"))}\'], [0], [$3\n], [])\nAT_CLEANUP\n])\n\nAT_BANNER([RPM version comparison])\n\nRPMVERCMP(1.0, 1.0, 0)\nRPMVERCMP(1.0, 2.0, -1)\nRPMVERCMP(2.0, 1.0, 1)\n\nRPMVERCMP(2.0.1, 2.0.1, 0)\nRPMVERCMP(2.0, 2.0.1, -1)\nRPMVERCMP(2.0.1, 2.0, 1)\n\nRPMVERCMP(2.0.1a, 2.0.1a, 0)\nRPMVERCMP(2.0.1a, 2.0.1, 1)\nRPMVERCMP(2.0.1, 2.0.1a, -1)\n\nRPMVERCMP(5.5p1, 5.5p1, 0)\nRPMVERCMP(5.5p1, 5.5p2, -1)\nRPMVERCMP(5.5p2, 5.5p1, 1)\n\nRPMVERCMP(5.5p10, 5.5p10, 0)\nRPMVERCMP(5.5p1, 5.5p10, -1)\nRPMVERCMP(5.5p10, 5.5p1, 1)\n\nRPMVERCMP(10xyz, 10.1xyz, -1)\nRPMVERCMP(10.1xyz, 10xyz, 1)\n\nRPMVERCMP(xyz10, xyz10, 0)\nRPMVERCMP(xyz10, xyz10.1, -1)\nRPMVERCMP(xyz10.1, xyz10, 1)\n\nRPMVERCMP(xyz.4, xyz.4, 0)\nRPMVERCMP(xyz.4, 8, -1)\nRPMVERCMP(8, xyz.4, 1)\nRPMVERCMP(xyz.4, 2, -1)\nRPMVERCMP(2, xyz.4, 1)\n\nRPMVERCMP(5.5p2, 5.6p1, -1)\nRPMVERCMP(5.6p1, 5.5p2, 1)\n\nRPMVERCMP(5.6p1, 6.5p1, -1)\nRPMVERCMP(6.5p1, 5.6p1, 1)\n\nRPMVERCMP(6.0.rc1, 6.0, 1)\nRPMVERCMP(6.0, 6.0.rc1, -1)\n\nRPMVERCMP(10b2, 10a1, 1)\nRPMVERCMP(10a2, 10b2, -1)\n\nRPMVERCMP(1.0aa, 1.0aa, 0)\nRPMVERCMP(1.0a, 1.0aa, -1)\nRPMVERCMP(1.0aa, 1.0a, 1)\n\nRPMVERCMP(10.0001, 10.0001, 0)\nRPMVERCMP(10.0001, 10.1, 0)\nRPMVERCMP(10.1, 10.0001, 0)\nRPMVERCMP(10.0001, 10.0039, -1)\nRPMVERCMP(10.0039, 10.0001, 1)\n\nRPMVERCMP(4.999.9, 5.0, -1)\nRPMVERCMP(5.0, 4.999.9, 1)\n\nRPMVERCMP(20101121, 20101121, 0)\nRPMVERCMP(20101121, 20101122, -1)\nRPMVERCMP(20101122, 20101121, 1)\n\nRPMVERCMP(2_0, 2_0, 0)\nRPMVERCMP(2.0, 2_0, 0)\nRPMVERCMP(2_0, 2.0, 0)\n\ndnl RhBug:178798 case\nRPMVERCMP(a, a, 0)\nRPMVERCMP(a+, a+, 0)\nRPMVERCMP(a+, a_, 0)\nRPMVERCMP(a_, a+, 0)\nRPMVERCMP(+a, +a, 0)\nRPMVERCMP(+a, _a, 0)\nRPMVERCMP(_a, +a, 0)\nRPMVERCMP(+_, +_, 0)\nRPMVERCMP(_+, +_, 0)\nRPMVERCMP(_+, _+, 0)\nRPMVERCMP(+, _, 0)\nRPMVERCMP(_, +, 0)\n\ndnl Basic testcases for tilde sorting\nRPMVERCMP(1.0~rc1, 1.0~rc1, 0)\nRPMVERCMP(1.0~rc1, 1.0, -1)\nRPMVERCMP(1.0, 1.0~rc1, 1)\nRPMVERCMP(1.0~rc1, 1.0~rc2, -1)\nRPMVERCMP(1.0~rc2, 1.0~rc1, 1)\nRPMVERCMP(1.0~rc1~git123, 1.0~rc1~git123, 0)\nRPMVERCMP(1.0~rc1~git123, 1.0~rc1, -1)\nRPMVERCMP(1.0~rc1, 1.0~rc1~git123, 1)\n\ndnl Basic testcases for caret sorting\nRPMVERCMP(1.0^, 1.0^, 0)\nRPMVERCMP(1.0^, 1.0, 1)\nRPMVERCMP(1.0, 1.0^, -1)\nRPMVERCMP(1.0^git1, 1.0^git1, 0)\nRPMVERCMP(1.0^git1, 1.0, 1)\nRPMVERCMP(1.0, 1.0^git1, -1)\nRPMVERCMP(1.0^git1, 1.0^git2, -1)\nRPMVERCMP(1.0^git2, 1.0^git1, 1)\nRPMVERCMP(1.0^git1, 1.01, -1)\nRPMVERCMP(1.01, 1.0^git1, 1)\nRPMVERCMP(1.0^20160101, 1.0^20160101, 0)\nRPMVERCMP(1.0^20160101, 1.0.1, -1)\nRPMVERCMP(1.0.1, 1.0^20160101, 1)\nRPMVERCMP(1.0^20160101^git1, 1.0^20160101^git1, 0)\nRPMVERCMP(1.0^20160102, 1.0^20160101^git1, 1)\nRPMVERCMP(1.0^20160101^git1, 1.0^20160102, -1)\n\ndnl Basic testcases for tilde and caret sorting\nRPMVERCMP(1.0~rc1^git1, 1.0~rc1^git1, 0)\nRPMVERCMP(1.0~rc1^git1, 1.0~rc1, 1)\nRPMVERCMP(1.0~rc1, 1.0~rc1^git1, -1)\nRPMVERCMP(1.0^git1~pre, 1.0^git1~pre, 0)\nRPMVERCMP(1.0^git1, 1.0^git1~pre, 1)\nRPMVERCMP(1.0^git1~pre, 1.0^git1, -1)\n\ndnl These are included here to document current, arguably buggy behaviors\ndnl for reference purposes and for easy checking against  unintended\ndnl behavior changes.\ndnl\ndnl AT_BANNER([RPM version comparison oddities])\ndnl RhBug:811992 case\ndnl RPMVERCMP(1b.fc17, 1b.fc17, 0)\ndnl RPMVERCMP(1b.fc17, 1.fc17, -1)\ndnl RPMVERCMP(1.fc17, 1b.fc17, 1)\ndnl RPMVERCMP(1g.fc17, 1g.fc17, 0)\ndnl RPMVERCMP(1g.fc17, 1.fc17, 1)\ndnl RPMVERCMP(1.fc17, 1g.fc17, -1)\n\ndnl Non-ascii characters are considered equal so these are all the same, eh...\ndnl RPMVERCMP(1.1.α, 1.1.α, 0)\ndnl RPMVERCMP(1.1.α, 1.1.β, 0)\ndnl RPMVERCMP(1.1.β, 1.1.α, 0)\ndnl RPMVERCMP(1.1.αα, 1.1.α, 0)\ndnl RPMVERCMP(1.1.α, 1.1.ββ, 0)\ndnl RPMVERCMP(1.1.ββ, 1.1.αα, 0)\n'

def convert(data):
    f = 'RPMVERCMP('
    lines = [ l for l in data.splitlines() if f in l ]
    tuples = [ tuple(c.strip() for c in l[len(f) + l.find(f):].rstrip(')').split(',')) for l in lines ]
    return [ (l, r, int(i)) for l, r, i in tuples ]


@pytest.fixture
def rpm_data():
    return convert(DEFAULT_DATA)


def test_rpm_vercmp(rpm_data):
    for l, r, expected in rpm_data:
        actual = _rpm_vercmp(l, r)
        assert actual == expected, (l, r, actual, expected)