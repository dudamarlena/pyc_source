# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/specs/jdr_archive.py
# Compiled at: 2019-05-16 13:41:33
"""
This module defines all datasources for JDR report
"""
from functools import partial
from insights.specs import Specs
from insights.core.plugins import datasource
from insights.core.context import JDRContext
from insights.core.spec_factory import simple_file, foreach_collect, first_file, glob_file, listdir
first_file = partial(first_file, context=JDRContext)
glob_file = partial(glob_file, context=JDRContext)
simple_file = partial(simple_file, context=JDRContext)
foreach_collect = partial(foreach_collect, context=JDRContext)

class JDRSpecs(Specs):
    """A class for all the JDR report datasources"""
    jboss_standalone_server_log = glob_file('JBOSS_HOME/standalone/log/server.log')

    @datasource(jboss_standalone_server_log, context=JDRContext, multi_output=True)
    def jboss_standalone_conf_file(broker):
        """Get which jboss standalone conf file is using from server log"""
        log_files = broker[JDRSpecs.jboss_standalone_server_log]
        if log_files:
            log_content = log_files[(-1)].content
            results = []
            for line in log_content:
                if 'sun.java.command =' in line and '.jdr' not in line and '-Djboss.server.base.dir' in line:
                    results.append(line)

            if results:
                config_xml = 'standalone.xml'
                java_command = results[(-1)]
                if '--server-config' in java_command:
                    config_xml = java_command.split('--server-config=')[1].split()[0]
                elif '-c ' in java_command:
                    config_xml = java_command.split('-c ')[1].split()[0]
                return [config_xml]
        return []

    jboss_standalone_main_config = foreach_collect(jboss_standalone_conf_file, 'JBOSS_HOME/standalone/configuration/%s')
    jboss_domain_servers = listdir('JBOSS_HOME/domain/servers/', context=JDRContext)
    jboss_domain_server_log = foreach_collect(jboss_domain_servers, 'JBOSS_HOME/domain/servers/%s/log/server.log')