# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/tests/test_logrotate.py
# Compiled at: 2019-05-28 16:54:55
# Size of source mod 2**32: 1924 bytes
from parsr.examples.logrotate_conf import loads
EXAMPLE = '\n# sample logrotate configuration file\ncompress\n\n/var/log/messages {\n    rotate 5\n    weekly\n    postrotate\n        /usr/bin/killall -HUP syslogd\n    endscript\n}\n\n"/var/log/httpd/access.log" /var/log/httpd/error.log {\n    rotate 5\n    mail www@my.org\n    size 100k\n    sharedscripts\n    postrotate\n        /usr/bin/killall -HUP httpd\n    endscript\n}\n\n/var/log/news/* {\n    monthly\n    rotate 2\n    olddir /var/log/news/old\n    missingok\n    postrotate\n        kill -HUP \'cat /var/run/inn.pid\'\n    endscript\n    nocompress\n}\n'.strip()
SIMPLE = '\n# sample logrotate configuration file\ncompress\n\n /var/log/messages {\n    rotate 5\n    weekly\n    postrotate\n        /usr/bin/killall -HUP syslogd\n    endscript\n}\n'

def test_logrotate_simple():
    res = loads(SIMPLE)
    if not 'compress' in res:
        raise AssertionError
    elif not '/var/log/messages' in res:
        raise AssertionError


def test_logrotate_example():
    res = loads(EXAMPLE)
    if not res['compress'].value is None:
        raise AssertionError
    else:
        if not res['/var/log/messages']['rotate'].value == 5:
            raise AssertionError
        else:
            if not res['/var/log/messages']['rotate'][0].lineno == 5:
                raise AssertionError
            elif not res['/var/log/messages']['weekly'].value is None:
                raise AssertionError
            assert res['/var/log/messages']['postrotate'].value == '/usr/bin/killall -HUP syslogd'
        assert res['/var/log/news/*'][0].lineno == 22


def xtest_logrotate_multikey():
    res = loads(EXAMPLE)
    if not res['compress'].value is None:
        raise AssertionError
    else:
        if not res['/var/log/httpd/access.log']['rotate'].value == 5:
            raise AssertionError
        else:
            if not res['/var/log/httpd/access.log']['size'].value == '100k':
                raise AssertionError
            else:
                if not res['/var/log/httpd/access.log']['sharedscripts'].value is None:
                    raise AssertionError
                elif not res['/var/log/httpd/error.log']['rotate'].value == 5:
                    raise AssertionError
                assert res['/var/log/httpd/error.log']['size'].value == '100k'
            assert res['/var/log/httpd/error.log']['sharedscripts'].value is None
        assert res['/var/log/news/*']['postrotate'].value == "kill -HUP 'cat /var/run/inn.pid'"