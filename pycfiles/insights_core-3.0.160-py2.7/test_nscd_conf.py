# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_nscd_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.nscd_conf import NscdConf, NscdConfLine
from insights.tests import context_wrap
NSCD_CONF = '\n#\n# /etc/nscd.conf\n#\n# An example Name Service Cache config file.  This file is needed by nscd.\n#\n# Legal entries are:\n#\n#       logfile                 <file>\n#       debug-level             <level>\n#       threads                 <initial #threads to use>\n#       max-threads             <maximum #threads to use>\n#       server-user             <user to run server as instead of root>\n#               server-user is ignored if nscd is started with -S parameters\n#       stat-user               <user who is allowed to request statistics>\n#       reload-count            unlimited|<number>\n#       paranoia                <yes|no>\n#       restart-interval        <time in seconds>\n#\n#       enable-cache            <service> <yes|no>\n#       positive-time-to-live   <service> <time in seconds>\n#       negative-time-to-live   <service> <time in seconds>\n#       suggested-size          <service> <prime number>\n#       check-files             <service> <yes|no>\n#       persistent              <service> <yes|no>\n#       shared                  <service> <yes|no>\n#       max-db-size             <service> <number bytes>\n#       auto-propagate          <service> <yes|no>\n#\n# Currently supported cache names (services): passwd, group, hosts, services\n#\n\n\n#       logfile                 /var/log/nscd.log\n#       threads                 4\n#       max-threads             32\n        server-user             nscd\n#       stat-user               somebody\n        debug-level             0\n#       reload-count            5\n        paranoia                no\n#       restart-interval        3600\n\n        enable-cache            passwd          no\n        positive-time-to-live   passwd          600\n        negative-time-to-live   passwd          20\n        suggested-size          passwd          211\n        check-files             passwd          yes\n        persistent              passwd          yes\n        shared                  passwd          yes\n        max-db-size             passwd          33554432\n        auto-propagate          passwd          yes\n\n        enable-cache            group           no\n        positive-time-to-live   group           3600\n        negative-time-to-live   group           60\n        suggested-size          group           211\n        check-files             group           yes\n        persistent              group           yes\n        shared                  group           yes\n        max-db-size             group           33554432\n        auto-propagate          group           yes\n\n        enable-cache            hosts           yes\n        positive-time-to-live   hosts           3600\n        negative-time-to-live   hosts           20\n        suggested-size          hosts           211\n        check-files             hosts           yes\n        persistent              hosts           yes\n        shared                  hosts           yes\n        max-db-size             hosts           33554432\n\n        enable-cache            services        yes\n        positive-time-to-live   services        28800\n        negative-time-to-live   services        20\n        suggested-size          services        211\n        check-files             services        yes\n        persistent              services        yes\n        shared                  services        yes\n        max-db-size             services        33554432\n\n        enable-cache            netgroup        no\n        positive-time-to-live   netgroup        28800\n        negative-time-to-live   netgroup        20\n        suggested-size          netgroup        211\n        check-files             netgroup        yes\n        persistent              netgroup        yes\n        shared                  netgroup        yes\n        max-db-size             netgroup        33554432\n\n'

def test_nscd_conf():
    conf = NscdConf(context_wrap(NSCD_CONF))
    assert conf is not None
    lines = [ l for l in conf ]
    assert len(lines) == 45
    assert len(conf.data) == 45
    assert lines[0] == conf.data[0]
    assert conf.service_attributes('bad-name') == []
    assert conf.service_attributes('hosts') == [
     NscdConfLine('enable-cache', 'hosts', 'yes'),
     NscdConfLine('positive-time-to-live', 'hosts', '3600'),
     NscdConfLine('negative-time-to-live', 'hosts', '20'),
     NscdConfLine('suggested-size', 'hosts', '211'),
     NscdConfLine('check-files', 'hosts', 'yes'),
     NscdConfLine('persistent', 'hosts', 'yes'),
     NscdConfLine('shared', 'hosts', 'yes'),
     NscdConfLine('max-db-size', 'hosts', '33554432')]
    assert conf.attribute('server-user') == 'nscd'
    assert conf.attribute('restart-interval') is None
    assert conf.filter('server-user') == [
     NscdConfLine(attribute='server-user', service=None, value='nscd')]
    assert conf.filter('log-file') == []
    assert conf.filter('enable-cache', 'netgroup') == [
     NscdConfLine(attribute='enable-cache', service='netgroup', value='no')]
    assert conf.filter('enable-cache') == [
     NscdConfLine(attribute='enable-cache', service='passwd', value='no'),
     NscdConfLine(attribute='enable-cache', service='group', value='no'),
     NscdConfLine(attribute='enable-cache', service='hosts', value='yes'),
     NscdConfLine(attribute='enable-cache', service='services', value='yes'),
     NscdConfLine(attribute='enable-cache', service='netgroup', value='no')]
    assert conf.filter('cache') == [
     NscdConfLine(attribute='enable-cache', service='passwd', value='no'),
     NscdConfLine(attribute='enable-cache', service='group', value='no'),
     NscdConfLine(attribute='enable-cache', service='hosts', value='yes'),
     NscdConfLine(attribute='enable-cache', service='services', value='yes'),
     NscdConfLine(attribute='enable-cache', service='netgroup', value='no')]
    return