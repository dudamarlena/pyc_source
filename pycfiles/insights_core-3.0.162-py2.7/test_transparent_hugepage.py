# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_transparent_hugepage.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.transparent_hugepage import ThpEnabled, ThpUseZeroPage
from insights.tests import context_wrap
ZEROPAGE_0 = '0'
ZEROPAGE_1 = '1'
ZEROPAGE_INVALID = '\nbla\nble\nasdf\n\n\n'
ENABLED_INVALID = '\n\nasdf fda asdfdsaf\n'
ENABLED_MADVISE = '\nalways [madvise] never\n'
ENABLED_NEVER = '\nalways madvise [never]\n'
ENABLED_ALWAYS = '[always] madvise never'

def test_zeropage():
    conf = ThpUseZeroPage(context_wrap(ZEROPAGE_0))
    assert conf is not None
    assert '0' == conf.use_zero_page
    conf = ThpUseZeroPage(context_wrap(ZEROPAGE_1))
    assert conf is not None
    assert '1' == conf.use_zero_page
    conf = ThpUseZeroPage(context_wrap(ZEROPAGE_INVALID))
    assert conf is not None
    assert ZEROPAGE_INVALID.replace('\n', ' ').strip() == conf.use_zero_page
    return


def test_enabled():
    conf = ThpEnabled(context_wrap(ENABLED_INVALID))
    assert conf is not None
    assert None is conf.active_option
    assert ENABLED_INVALID.strip() == conf.line
    conf = ThpEnabled(context_wrap(ENABLED_MADVISE))
    assert conf is not None
    assert 'madvise' == conf.active_option
    assert ENABLED_MADVISE.strip() == conf.line
    conf = ThpEnabled(context_wrap(ENABLED_NEVER))
    assert conf is not None
    assert 'never' == conf.active_option
    assert ENABLED_NEVER.strip() == conf.line
    conf = ThpEnabled(context_wrap(ENABLED_ALWAYS))
    assert conf is not None
    assert 'always' == conf.active_option
    assert ENABLED_ALWAYS.strip() == conf.line
    return