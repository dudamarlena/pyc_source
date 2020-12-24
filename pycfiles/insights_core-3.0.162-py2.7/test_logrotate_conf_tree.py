# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_logrotate_conf_tree.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr.query import first
from insights.combiners.logrotate_conf import _LogRotateConf, LogRotateConfTree
from insights.tests import context_wrap
CONF = ('\n# see "man logrotate" for details\n# rotate log files weekly\nweekly\n\n# keep 4 weeks worth of backlogs\nrotate 4\n\n# create new (empty) log files after rotating old ones\ncreate\n\n# use date as a suffix of the rotated file\ndateext\n\n# uncomment this if you want your log files compressed\n#compress\n\n# RPM packages drop log rotation information into this directory\ninclude /etc/logrotate.d\n\n# no packages own wtmp and btmp -- we\'ll rotate them here\n/var/log/wtmp {\n    missingok\n    monthly\n    create 0664 root utmp\n    minsize 1M\n    rotate 1\n    postrotate\n        do some stuff to wtmp\n    endscript\n}\n\n/var/log/btmp {\n    missingok\n    monthly\n    create 0600 root utmp\n    postrotate\n        do some stuff to btmp\n    endscript\n    rotate 1\n}\n\n# system-specific logs may be also be configured here.\n').strip()
JUNK_SPACE = ('\n#SEG_15.06.01\xa0\n/var/log/spooler\n{\n    compress\n    missingok\n    rotate 30\n    size 1M\n    sharedscripts\n    postrotate\n        /bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true\n    endscript\n}\n').strip()

def test_logrotate_tree():
    p = _LogRotateConf(context_wrap(CONF, path='/etc/logrotate.conf'))
    conf = LogRotateConfTree([p])
    assert len(conf['weekly']) == 1
    assert len(conf['/var/log/wtmp']['missingok']) == 1
    assert conf['/var/log/wtmp']['postrotate'][first].value == 'do some stuff to wtmp'
    assert len(conf['/var/log/btmp']['rotate']) == 1
    assert len(conf['/var/log/btmp']['postrotate']) == 1
    assert conf['/var/log/btmp']['postrotate'][first].value == 'do some stuff to btmp'


def test_junk_space():
    p = _LogRotateConf(context_wrap(JUNK_SPACE, path='/etc/logrotate.conf'))
    conf = LogRotateConfTree([p])
    assert 'compress' in conf['/var/log/spooler']