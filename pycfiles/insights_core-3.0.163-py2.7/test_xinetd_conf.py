# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_xinetd_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.xinetd_conf import XinetdConf
from insights.tests import context_wrap
XINETD_CONF_0 = '\ndefaults\n{\n}\n\nincludedir /etc/xinetd.d\n'
XINETD_CONF_1 = '\ndefaults\n{\n# The next two items are intended to be a quick access place to\n# temporarily enable or disable services.\n#\n#\tenabled\t\t=\n#\tdisabled\t=\n        enabled         =\n\n# Define general logging characteristics.\n        log_type\t= SYSLOG daemon info\n        log_on_failure\t= HOST\n        log_on_success\t= PID HOST DURATION EXIT\n\n# Define access restriction defaults\n#\n#\tno_access\t=\n#\tonly_from\t=\n#\tmax_load\t= 0\n        cps\t\t= 50 10\n        instances\t= 50\n        per_source\t= 10\n\n# Address and networking defaults\n#\n#\tbind\t\t=\n#\tmdns\t\t= yes\n        v6only\t\t= no\n\n# setup environmental attributes\n#\n#\tpassenv\t\t=\n        groups\t\t= yes\n        umask\t\t= 002\n\n# Generally, banners are not used. This sets up their global defaults\n#\n#\tbanner\t\t=\n#\tbanner_fail\t=\n#\tbanner_success\t=\n}\n\nincludedir /etc/xinetd.d\n'
XINETD_CONF_2_BAD = '\ndefaults {\n        umask\t\t= 002\n}\n\nincludedir /etc/xinetd.d\n'
XINETD_CONF_3_BAD = '\ndefaults\n{\n        umask\t\t= 002\n}\n\nbalabala...\n\nincludedir /etc/xinetd.d\n'
XINETD_CONF_4_BAD = '\ndefaults {\n        umask\t\t002\n}\n\nincludedir /etc/xinetd.d\n'
XINETD_CONF_5 = '\ndefaults\n{\n        umask\t\t= 002\n}\n\nincludedir /etc/xinetd.d/abc\n'
XINETD_CONF_6 = '\ndefaults\n{\n        umask\t\t= 002\n}\n'
XINETD_D_TFTP = '\nservice tftp\n{\n        socket_type             = dgram\n        protocol                = udp\n        wait                    = yes\n        user                    = root\n        server                  = /usr/sbin/in.tftpd\n        server_args             = -s /var/lib/tftpboot\n        disable                 = yes\n        per_source              = 11\n        cps                     = 100 2\n        flags                   = IPv4\n}\n'
CONF_PATH = '/etc/xinetd.conf'
D_TFTP_PATH = '/etc/xinetd.d/tftp'

def test_XinetdConf_0():
    xinetd_conf = XinetdConf(context_wrap(XINETD_CONF_0, path=CONF_PATH))
    data = xinetd_conf.data
    assert xinetd_conf.is_valid
    assert xinetd_conf.is_includedir
    assert data.get('includedir') == '/etc/xinetd.d'
    assert data.get('defaults') == {}


def test_XinetdConf_1():
    xinetd_conf = XinetdConf(context_wrap(XINETD_CONF_1, path=CONF_PATH))
    data = xinetd_conf.data
    assert xinetd_conf.is_valid
    assert xinetd_conf.is_includedir
    assert data.get('includedir') == '/etc/xinetd.d'
    assert data.get('defaults') == {'enabled': '', 
       'v6only': 'no', 
       'log_on_failure': 'HOST', 
       'umask': '002', 
       'log_on_success': 'PID HOST DURATION EXIT', 
       'instances': '50', 
       'per_source': '10', 
       'groups': 'yes', 
       'cps': '50 10', 
       'log_type': 'SYSLOG daemon info'}
    assert xinetd_conf.file_name == 'xinetd.conf'
    assert xinetd_conf.file_path == CONF_PATH


def test_XinetdConf_tftp():
    d_tftp = XinetdConf(context_wrap(XINETD_D_TFTP, path=D_TFTP_PATH))
    data = d_tftp.data
    assert d_tftp.is_valid
    assert not d_tftp.is_includedir
    assert data.get('includedir') is None
    assert data.get('tftp') == {'protocol': 'udp', 
       'socket_type': 'dgram', 
       'server': '/usr/sbin/in.tftpd', 
       'server_args': '-s /var/lib/tftpboot', 
       'disable': 'yes', 
       'flags': 'IPv4', 
       'user': 'root', 
       'per_source': '11', 
       'cps': '100 2', 
       'wait': 'yes'}
    assert d_tftp.file_name == 'tftp'
    assert d_tftp.file_path == D_TFTP_PATH
    return


def test_XinetdConf_2():
    xinetd_conf = XinetdConf(context_wrap(XINETD_CONF_2_BAD, path=CONF_PATH))
    assert not xinetd_conf.is_valid


def test_XinetdConf_3():
    xinetd_conf = XinetdConf(context_wrap(XINETD_CONF_3_BAD, path=CONF_PATH))
    assert not xinetd_conf.is_valid


def test_XinetdConf_4():
    xinetd_conf = XinetdConf(context_wrap(XINETD_CONF_4_BAD, path=CONF_PATH))
    assert not xinetd_conf.is_valid


def test_XinetdConf_5():
    xinetd_conf = XinetdConf(context_wrap(XINETD_CONF_5, path=CONF_PATH))
    data = xinetd_conf.data
    assert xinetd_conf.is_valid
    assert not xinetd_conf.is_includedir
    assert data.get('includedir') == '/etc/xinetd.d/abc'
    assert data.get('defaults') == {'umask': '002'}