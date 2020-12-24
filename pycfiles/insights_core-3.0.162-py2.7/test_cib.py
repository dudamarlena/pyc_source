# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cib.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.cib import CIB
from insights.tests import context_wrap
CIB_CONFIG = '\n    <cib crm_feature_set="3.0.9" validate-with="pacemaker-2.3" have-quorum="1" dc-uuid="4">\n      <configuration>\n        <crm_config>\n          <cluster_property_set id="cib-bootstrap-options">\n            <nvpair id="cib-bootstrap-options-have-watchdog" name="have-watchdog" value="false"/>\n            <nvpair id="cib-bootstrap-options-no-quorum-policy" name="no-quorum-policy" value="freeze"/>\n          </cluster_property_set>\n        </crm_config>\n        <nodes>\n          <node id="1" uname="foo"/>\n          <node id="2" uname="bar"/>\n          <node id="3" uname="baz"/>\n        </nodes>\n        <resources>\n          <clone id="dlm-clone">\n          </clone>\n        </resources>\n        <constraints>\n          <rsc_order first="dlm-clone" first-action="start" id="order-dlm-clone-clvmd-clone-mandatory" then="clvmd-clone" then-action="start"/>\n          <rsc_colocation id="colocation-clvmd-clone-dlm-clone-INFINITY" rsc="clvmd-clone" score="INFINITY" with-rsc="dlm-clone"/>\n        </constraints>\n      </configuration>\n    </cib>\n'

def test_cib():
    cib = CIB(context_wrap(CIB_CONFIG))
    assert cib is not None
    assert cib.nodes == ['foo', 'bar', 'baz']
    return