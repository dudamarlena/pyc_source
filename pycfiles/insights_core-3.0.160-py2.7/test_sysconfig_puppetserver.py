# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_puppetserver.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import PuppetserverSysconfig
from insights.tests import context_wrap
PUPPETSERVER_CONFIG = '\n###########################################\n# Init settings for puppetserver\n###########################################\n\n# Location of your Java binary (version 7 or higher)\nJAVA_BIN="/usr/bin/java"\n\n# Modify this if you\'d like to change the memory allocation, enable JMX, etc\nJAVA_ARGS="-Xms2g -Xmx2g -XX:MaxPermSize=256m"\n\n# These normally shouldn\'t need to be edited if using OS packages\nUSER="puppet"\nGROUP="puppet"\nINSTALL_DIR="/opt/puppetlabs/server/apps/puppetserver"\nCONFIG="/etc/puppetlabs/puppetserver/conf.d"\n\n# Bootstrap path\nBOOTSTRAP_CONFIG="/etc/puppetlabs/puppetserver/services.d/,/opt/puppetlabs/server/apps/puppetserver/config/services.d/"\n\n# SERVICE_STOP_RETRIES can be set here to alter the default stop timeout in\n# seconds.  For systemd, the shorter of this setting or \'TimeoutStopSec\' in\n# the systemd.service definition will effectively be the timeout which is used.\nSERVICE_STOP_RETRIES=60\n\n# START_TIMEOUT can be set here to alter the default startup timeout in\n# seconds.  For systemd, the shorter of this setting or \'TimeoutStartSec\'\n# in the service\'s systemd.service configuration file will effectively be the\n# timeout which is used.\nSTART_TIMEOUT=300\n\n\n# Maximum number of seconds that can expire for a service reload attempt before\n# the result of the attempt is interpreted as a failure.\nRELOAD_TIMEOUT=120\n'

def test_puppetserver_config():
    puppetserver_config = PuppetserverSysconfig(context_wrap(PUPPETSERVER_CONFIG))
    assert puppetserver_config['GROUP'] == 'puppet'
    assert puppetserver_config.get('START_TIMEOUT') == '300'
    assert len(puppetserver_config.keys()) == 10