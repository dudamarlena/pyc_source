# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rhn_hibernate_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.rhn_hibernate_conf import RHNHibernateConf
conf_content = ("\n############################################################################\n## HIBERNATE CONFIGURATION\n##\n## This is not the only way to configure hibernate.  You can\n## create a hibernate.cfg.xml file or you can create your own\n## custom file which you parse and create a new Configuration object.\n##\n## We're using the hibernate.properties file because it's simple.\n############################################################################\nhibernate.dialect=org.hibernate.dialect.Oracle10gDialect\nhibernate.connection.driver_class=oracle.jdbc.driver.OracleDriver\nhibernate.connection.driver_proto=\nhibernate.connection.provider_class=org.hibernate.connection.C3P0ConnectionProvider\n\nhibernate.use_outer_join=true\nhibernate.jdbc.batch_size=0\n#hibernate.show_sql=true\n\nhibernate.c3p0.min_size=5\nhibernate.c3p0.max_size=20\nhibernate.c3p0.timeout=300\n#\n# This should always be 0.\n#\nhibernate.c3p0.max_statements=0\n\n# test period value in seconds\nhibernate.c3p0.idle_test_period=300\nhibernate.c3p0.testConnectionOnCheckout=true\nhibernate.c3p0.connectionCustomizerClassName=com.redhat.rhn.common.db.RhnConnectionCustomizer\nhibernate.c3p0.preferredTestQuery=select 'c3p0 ping' from dual\n\nhibernate.cache.provider_class=org.hibernate.cache.OSCacheProvider\nhibernate.cache.use_query_cache=true\nhibernate.bytecode.use_reflection_optimizer=false\nhibernate.jdbc.batch_size=0\n").strip()

def test_rhn_hibernate_conf():
    result = RHNHibernateConf(context_wrap(conf_content))
    assert result.get('hibernate.c3p0.max_statements') == '0'
    assert result.get('hibernate.connection.driver_proto') == ''
    assert result.get('hibernate.c3p0.preferredTestQuery') == "select 'c3p0 ping' from dual"