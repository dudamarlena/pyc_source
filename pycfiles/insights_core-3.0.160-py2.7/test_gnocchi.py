# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_gnocchi.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import gnocchi
from insights.parsers.gnocchi import GnocchiConf, GnocchiMetricdLog
from insights.tests import context_wrap
from datetime import datetime
GNOCCHI_CONF = ('\n[DEFAULT]\nlog_dir = /var/log/gnocchi\n[api]\nauth_mode = keystone\nmax_limit = 1000\n[archive_policy]\n[indexer]\nurl = mysql+pymysql://gnocchi:exampleabckeystring@192.168.0.1/gnocchi?charset=utf8\n[metricd]\nworkers = 2\n[oslo_middleware]\n[oslo_policy]\npolicy_file = /etc/gnocchi/policy.json\n[statsd]\nresource_id = 5e3fcbe2-7aab-475d-b42c-abcdefgh\nuser_id = e0ca4711-1128-422c-abd6-abcdefgh\nproject_id = af0c88e8-90d8-4795-9efe-abcdefgh\narchive_policy_name = high\nflush_delay = 10\n[storage]\ndriver = file\n#this one comment\nfile_basepath = /var/lib/gnocchi\n[keystone_authtoken]\nauth_uri=http://192.168.0.1:5000/v3\nauth_type=password\nauth_version=v3\nauth_url=http://192.168.0.1:35357\nusername=gnocchi\npassword=yourpassword23432\nuser_domain_name=Default\nproject_name=services\nproject_domain_name=Default\n').strip()
METRICD_LOG = '\n2017-04-12 03:10:53.076 14550 INFO gnocchi.cli [-] 0 measurements bundles across 0 metrics wait to be processed.\n2017-04-12 03:12:53.078 14550 INFO gnocchi.cli [-] 0 measurements bundles across 0 metrics wait to be processed.\n2017-04-12 03:14:53.080 14550 INFO gnocchi.cli [-] 0 measurements bundles across 0 metrics wait to be processed.\n2017-04-13 21:06:11.676 114807 ERROR tooz.drivers.redis ToozError: Cannot extend an unlocked lock\n'

def test_gnocchi_conf():
    gnocchi_conf = GnocchiConf(context_wrap(GNOCCHI_CONF))
    assert sorted(gnocchi_conf.sections()) == sorted(['api', 'archive_policy', 'indexer', 'metricd', 'oslo_middleware', 'oslo_policy', 'statsd', 'storage', 'keystone_authtoken'])
    assert 'storage' in gnocchi_conf.sections()
    assert gnocchi_conf.has_option('indexer', 'url')
    assert gnocchi_conf.get('indexer', 'url') == 'mysql+pymysql://gnocchi:exampleabckeystring@192.168.0.1/gnocchi?charset=utf8'
    assert gnocchi_conf.getint('statsd', 'flush_delay') == 10


def test_metrics_log():
    log = GnocchiMetricdLog(context_wrap(METRICD_LOG))
    assert len(log.get('INFO')) == 3
    assert 'measurements bundles across 0 metrics wait to be processed' in log
    assert log.get('ERROR') == [{'raw_message': '2017-04-13 21:06:11.676 114807 ERROR tooz.drivers.redis ToozError: Cannot extend an unlocked lock'}]
    assert len(list(log.get_after(datetime(2017, 4, 12, 19, 36, 38)))) == 1
    assert list(log.get_after(datetime(2017, 4, 12, 19, 36, 38))) == [{'raw_message': '2017-04-13 21:06:11.676 114807 ERROR tooz.drivers.redis ToozError: Cannot extend an unlocked lock'}]


def test_doc():
    env = {'GnocchiConf': GnocchiConf, 
       'conf': GnocchiConf(context_wrap(GNOCCHI_CONF, path='/etc/gnocchi/gnocchi.conf')), 
       'GnocchiMetricdLog': GnocchiMetricdLog, 
       'log': GnocchiMetricdLog(context_wrap(METRICD_LOG, path='/etc/gnocchi/metricd.log'))}
    failed, total = doctest.testmod(gnocchi, globs=env)
    assert failed == 0