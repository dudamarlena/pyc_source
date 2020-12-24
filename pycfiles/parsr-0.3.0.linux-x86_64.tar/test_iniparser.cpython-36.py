# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/tests/test_iniparser.py
# Compiled at: 2019-05-30 12:36:47
# Size of source mod 2**32: 1101 bytes
from parsr.examples.iniparser import parse_doc
DATA = "\n[DEFAULT]\ntrooper_guns = miss\n\n[global]\nlogging=debug\nlog=/var/logs/sample.log\n\n# Keep this info secret\n[secret_stuff]\nusername=dvader\npassword=luke_is_my_son\n\n[facts]\nmajor_vulnerability=ray-shielded particle exhaust vent\nvader = definitely Luke's\n    father\n\n[settings]\nmusic=The Imperial March\ncolor=blue\n#blah\ncolor=black\naccuracy=0\nbanks=0 1 2\n\n[novalue]\nthe_force\n\n".strip()

def test_iniparser():
    res = parse_doc(DATA, None)
    assert len(res) == 5


def test_hanging_indent():
    res = parse_doc(DATA, None)
    assert res['facts']['vader'][0].value == "definitely Luke's father"


def test_defaults():
    res = parse_doc(DATA, None)
    assert res['facts']['trooper_guns'][0].value == 'miss'


def test_multiple_values():
    res = parse_doc(DATA, None)
    if not len(res['settings']['color']) == 2:
        raise AssertionError
    else:
        assert res['settings']['accuracy'][0].value == '0'
        assert res['settings']['banks'][0].value == '0 1 2'


def test_no_value():
    res = parse_doc(DATA, None)
    assert res['novalue']['the_force'][0].value is None