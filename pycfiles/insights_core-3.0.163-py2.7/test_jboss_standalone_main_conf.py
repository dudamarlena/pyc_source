# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_jboss_standalone_main_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.jboss_standalone_main_conf import JbossStandaloneConf
from insights.tests import context_wrap
from insights.parsers import jboss_standalone_main_conf
import doctest
JBOSS_STANDALONE_CONFIG = '\n<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n\n<server xmlns="urn:jboss:domain:1.7">\n    <management>\n        <security-realms>\n            <security-realm name="ManagementRealm">\n                <authentication>\n                    <local default-user="$local" skip-group-loading="true"/>\n                    <properties path="mgmt-users.properties" relative-to="jboss.server.config.dir"/>\n                </authentication>\n                <authorization map-groups-to-roles="false">\n                    <properties path="mgmt-groups.properties" relative-to="jboss.server.config.dir"/>\n                </authorization>\n            </security-realm>\n            <security-realm name="ApplicationRealm">\n                <authentication>\n                    <local default-user="$local" allowed-users="*" skip-group-loading="true"/>\n                    <properties path="application-users.properties" relative-to="jboss.server.config.dir"/>\n                </authentication>\n                <authorization>\n                    <properties path="application-roles.properties" relative-to="jboss.server.config.dir"/>\n                </authorization>\n            </security-realm>\n        </security-realms>\n        <audit-log>\n            <formatters>\n                <json-formatter name="json-formatter"/>\n            </formatters>\n            <handlers>\n                <file-handler name="file" formatter="json-formatter" path="audit-log.log" relative-to="jboss.server.data.dir"/>\n            </handlers>\n            <logger log-boot="true" log-read-only="false" enabled="false">\n                <handlers>\n                    <handler name="file"/>\n                </handlers>\n            </logger>\n        </audit-log>\n        <management-interfaces>\n            <native-interface security-realm="ManagementRealm">\n                <socket-binding native="management-native"/>\n            </native-interface>\n            <http-interface security-realm="ManagementRealm">\n                <socket-binding http="management-http"/>\n            </http-interface>\n        </management-interfaces>\n        <access-control provider="simple">\n            <role-mapping>\n                <role name="SuperUser">\n                    <include>\n                        <user name="$local"/>\n                    </include>\n                </role>\n            </role-mapping>\n        </access-control>\n    </management>\n</server>\n'

def test_jboss_standalone_conf():
    jboss_standalone_conf = JbossStandaloneConf(context_wrap(JBOSS_STANDALONE_CONFIG, path='/root/jboss/jboss-eap-6.4/standalone/configuration/standalone.xml'))
    assert jboss_standalone_conf is not None
    assert jboss_standalone_conf.file_path == '/root/jboss/jboss-eap-6.4/standalone/configuration/standalone.xml'
    assert jboss_standalone_conf.get_elements('.//management/security-realms/security-realm/authentication/properties')[0].get('relative-to') == 'jboss.server.config.dir'
    return


def test_jboss_standalone_conf_doc_examples():
    env = {'JbossStandaloneConf': JbossStandaloneConf, 
       'jboss_main_config': JbossStandaloneConf(context_wrap(JBOSS_STANDALONE_CONFIG, path='/root/jboss/jboss-eap-6.4/standalone/configuration/standalone.xml'))}
    failed, total = doctest.testmod(jboss_standalone_main_conf, globs=env)
    assert failed == 0