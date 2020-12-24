# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/evaluation/test/res/ipap_example.py
# Compiled at: 2019-08-19 15:09:29
"""
Examples on using the evaluation scheme for exposing icepap driver values
as taurus attributes
"""
from __future__ import print_function
ATTR_IPAP_POS = 'eval:@ipap=pyIcePAP.EthIcePAP("icepap06", port=5000)' + '/float(ipap.readParameter(1,"POS"))'

def _test1():
    import taurus.core
    a = taurus.Attribute(ATTR_IPAP_POS)
    print('axis pos:', a.read().rvalue)


def _test2():
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    from taurus.qt.qtgui.display import TaurusLabel
    app = TaurusApplication(cmd_line_parser=None)
    tl = TaurusLabel()
    tl.setModel(ATTR_IPAP_POS)
    tl.show()
    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    _test1()
    _test2()