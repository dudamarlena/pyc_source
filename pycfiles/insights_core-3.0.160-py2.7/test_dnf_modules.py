# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_dnf_modules.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import dnf_modules
from insights.tests import context_wrap
DNF_MODULES_INPUT = '\n[postgresql]\nname=postgresql\nprofiles=client\nstate=enabled\nstream=9.6\n[python36]\nname=python36\nprofiles=\nstate=enabled\nstream=3.6\n[virt]\nname=virt\nprofiles=\nstate=enabled\nstream=rhel\n'

def test_dnf_modules():
    modules_config = dnf_modules.DnfModules(context_wrap(DNF_MODULES_INPUT))
    assert modules_config is not None
    assert 'postgresql' in modules_config.sections()
    assert 'python36' in modules_config.sections()
    assert 'virt' in modules_config.sections()
    assert 'enabled' == modules_config.get('postgresql', 'state')
    return


def test_dnf_modules_doc_examples():
    failed, total = doctest.testmod(dnf_modules, globs={'dnf_modules': dnf_modules.DnfModules(context_wrap(DNF_MODULES_INPUT))})
    assert failed == 0