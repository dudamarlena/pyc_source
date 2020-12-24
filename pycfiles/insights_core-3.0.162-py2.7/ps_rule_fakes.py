# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/plugins/ps_rule_fakes.py
# Compiled at: 2020-03-25 13:10:41
from insights import rule, make_pass
from insights.core.filters import add_filter
from insights.parsers.ps import PsAux, PsAuxww, PsAlxwww
from insights.specs import Specs

@rule(PsAux)
def psaux_no_filter(ps_aux):
    return make_pass('FAKE RESULT')


add_filter(Specs.ps_auxww, 'fake-filter')

@rule(PsAuxww)
def psauxww_ds_filter(ps_auxww):
    return make_pass('FAKE RESULT')


add_filter(PsAlxwww, 'fake-filter')

@rule(PsAlxwww)
def psalxwww_parser_filter(ps_alxwww):
    return make_pass('FAKE RESULT')