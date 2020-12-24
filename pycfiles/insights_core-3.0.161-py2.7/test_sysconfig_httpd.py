# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_httpd.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.sysconfig import HttpdSysconfig
HTTPD = ("\n# Configuration file for the httpd service.\n\n#\n# The default processing model (MPM) is the process-based\n# 'prefork' model.  A thread-based model, 'worker', is also\n# available, but does not work with some modules (such as PHP).\n# The service must be stopped before changing this variable.\n#\nHTTPD=/usr/sbin/httpd.worker\n\n#\n# To pass additional options (for instance, -D definitions) to the\n# httpd binary at startup, set OPTIONS here.\n#\n#OPTIONS=\nOPTIONS1=\n#\n# By default, the httpd process is started in the C locale; to\n# change the locale in which the server runs, the HTTPD_LANG\n# variable can be set.\n#\nHTTPD_LANG=C\n").strip()

def test_httpd_service_conf():
    result = HttpdSysconfig(context_wrap(HTTPD))
    assert result['HTTPD'] == '/usr/sbin/httpd.worker'
    assert result.get('OPTIONS') is None
    assert result.get('OPTIONS1') == ''
    assert result['HTTPD_LANG'] == 'C'
    return