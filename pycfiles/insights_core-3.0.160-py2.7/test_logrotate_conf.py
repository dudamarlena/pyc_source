# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_logrotate_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import logrotate_conf
from insights.parsers.logrotate_conf import LogrotateConf
from insights.tests import context_wrap
import doctest
LOGROTATE_CONF_1 = ('\n# see "man logrotate" for details\n# rotate log files weekly\nweekly\n\n# keep 4 weeks worth of backlogs\nrotate 4\n\n# create new (empty) log files after rotating old ones\ncreate\n\n# use date as a suffix of the rotated file\ndateext\n\n# uncomment this if you want your log files compressed\n#compress\n\n# RPM packages drop log rotation information into this directory\ninclude /etc/logrotate.d\n\n# no packages own wtmp and btmp -- we\'ll rotate them here\n/var/log/wtmp {\n    monthly\n    create 0664 root utmp\n        minsize 1M\n    rotate 1\n}\n').strip()
LOGROTATE_CONF_2 = ('\n#1343753: cant use * here cause not all logs in this folder will be owned by tomcat\n/var/log/candlepin/access.log /var/log/candlepin/audit.log /var/log/candlepin/candlepin.log /var/log/candlepin/error.log {\n# logrotate 3.8 requires the su directive,\n# where as prior versions do not recognize it.\n#LOGROTATE-3.8#    su tomcat tomcat\n    copytruncate\n    daily\n    rotate 52\n    compress\n    missingok\n    create 0644 tomcat tomcat\n}\n').strip()
LOGROTATE_CONF_3 = ('\n/var/log/cron\n/var/log/maillog\n/var/log/messages\n/var/log/secure\n/var/log/spooler\n{\n    sharedscripts\n    postrotate\n        /bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true\n    endscript\n}\n').strip()
LOGROTATE_MAN_PAGE_DOC = ('\n# sample file\ncompress\n\n/var/log/messages {\n    rotate 5\n    weekly\n    postrotate\n                /sbin/killall -HUP syslogd\n    endscript\n}\n\n"/var/log/httpd/access.log" /var/log/httpd/error.log {\n    rotate 5\n    mail www@my.org\n    size=100k\n    sharedscripts\n    postrotate\n                /sbin/killall -HUP httpd\n    endscript\n}\n\n/var/log/news/news.crit\n/var/log/news/olds.crit  {\n    monthly\n    rotate 2\n    olddir /var/log/news/old\n    missingok\n    postrotate\n                kill -HUP `cat /var/run/inn.pid`\n    endscript\n    nocompress\n}\n').strip()

def test_web_xml_doc_examples():
    env = {'log_rt': LogrotateConf(context_wrap(LOGROTATE_MAN_PAGE_DOC, path='/etc/logrotate.conf'))}
    failed, total = doctest.testmod(logrotate_conf, globs=env)
    assert failed == 0


def test_logrotate_conf_1():
    log_rt = LogrotateConf(context_wrap(LOGROTATE_CONF_1, path='/etc/logrotate.conf'))
    assert 'compress' not in log_rt.options
    assert log_rt['include'] == '/etc/logrotate.d'
    assert log_rt['/var/log/wtmp']['minsize'] == '1M'
    assert log_rt.log_files == ['/var/log/wtmp']
    assert log_rt['/var/log/wtmp']['create'] == '0664 root utmp'


def test_logrotate_conf_2():
    log_rt = LogrotateConf(context_wrap(LOGROTATE_CONF_2, path='/etc/logrotate.conf'))
    assert log_rt.options == []
    assert '/var/log/candlepin/access.log' in log_rt.log_files
    assert log_rt['/var/log/candlepin/access.log']['rotate'] == '52'
    assert log_rt['/var/log/candlepin/error.log']['missingok'] is True
    assert log_rt['/var/log/candlepin/audit.log']['create'] == '0644 tomcat tomcat'


def test_logrotate_conf_3():
    log_rt = LogrotateConf(context_wrap(LOGROTATE_CONF_3, path='/etc/logrotate.conf'))
    assert log_rt.options == []
    assert '/var/log/maillog' in log_rt.log_files
    assert log_rt['/var/log/cron']['sharedscripts'] is True
    assert log_rt['/var/log/messages']['postrotate'] == [
     '/bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true']