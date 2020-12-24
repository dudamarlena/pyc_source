# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/tests/test_iniparser.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr.iniparser import parse_doc
DATA = ("\n[DEFAULT]\ntrooper_guns = miss\n\n[global]\nlogging=debug\nlog=/var/logs/sample.log\n\n# Keep this info secret\n[secret_stuff]\nusername=dvader\npassword=luke_is_my_son\n\n[facts]\nmajor_vulnerability=ray-shielded particle exhaust vent\nvader = definitely Luke's\n    father\n\n[settings]\nmusic=The Imperial March\ncolor=blue\n#blah\ncolor=black\naccuracy=0\nbanks=0 1 2\n\n[novalue]\nthe_force\n\n").strip()

def test_iniparser():
    res = parse_doc(DATA, None)
    assert len(res) == 5
    return


def test_hanging_indent():
    res = parse_doc(DATA, None)
    assert res['facts']['vader'][0].value == "definitely Luke's father"
    return


def test_defaults():
    res = parse_doc(DATA, None)
    assert res['facts']['trooper_guns'][0].value == 'miss'
    return


def test_multiple_values():
    res = parse_doc(DATA, None)
    assert len(res['settings']['color']) == 2
    assert res['settings']['accuracy'][0].value == '0'
    assert res['settings']['banks'][0].value == '0 1 2'
    return


def test_no_value():
    res = parse_doc(DATA, None)
    assert res['novalue']['the_force'][0].value is None
    return