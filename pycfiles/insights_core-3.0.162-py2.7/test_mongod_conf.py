# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_mongod_conf.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.tests import context_wrap
from insights.parsers import ParseException
from insights.parsers.mongod_conf import MongodbConf
NORMAL_CONF = ('\n# mongodb.conf - generated from Puppet\n\n#where to log\nlogpath=/var/log/mongodb/mongodb.log\nlogappend=true\n# Set this option to configure the mongod or mongos process to bind to and\n# listen for connections from applications on this address.\n# You may concatenate a list of comma separated values to bind mongod to multiple IP addresses.\nbind_ip = 127.0.0.1\n# fork and run in background\nfork=true\ndbpath=/var/lib/mongodb\n# location of pidfile\npidfilepath=/var/run/mongodb/mongodb.pid\n# Enables journaling\njournal = true\n# Turn on/off security.  Off is currently the default\nnoauth=true\nabc=\n').strip()
NORMAL_CONF_V1 = ('\n=/var/log/mongodb/mongodb.log\nlogappend=true # noauth=true\n').strip()
YAML_CONF = ('\n# mongod.conf\n\n# for documentation of all options, see:\n#   http://docs.mongodb.org/manual/reference/configuration-options/\n\n# where to write logging data.\nsystemLog:\n  destination: file\n  logAppend: true\n  path: /var/log/mongodb/mongod.log\n\n# Where and how to store data.\nstorage:\n  dbPath: /var/lib/mongo\n  journal:\n    enabled: true\n#  engine:\n#  mmapv1:\n#  wiredTiger:\n\n# how the process runs\nprocessManagement:\n  fork: true  # fork and run in background\n  pidFilePath: /var/run/mongodb/mongod.pid  # location of pidfile\n\n# network interfaces\nnet:\n  port: 27017\n  #bindIp: 127.0.0.1  # Listen to local interface only, comment to listen on all interfaces.\n  #bindIp: 127.0.0.1  # Listen to local interface only, comment to listen on all interfaces.\n\n\n#security:\n\n#operationProfiling:\n\n#replication:\n\n#sharding:\n\n## Enterprise-Only Options\n\n#auditLog:\n\n#snmp:\n').strip()
YAML_CONF_UNPARSABLE = ('\nsystemLog:\n  destination: file\n  logAppend: true\n  port=27017\n\n').strip()

def test_mongodb_conf():
    result = MongodbConf(context_wrap(YAML_CONF))
    assert result.get('security') is None
    assert result.get('processManagement') == {'fork': True, 
       'pidFilePath': '/var/run/mongodb/mongod.pid'}
    assert result.is_yaml is True
    assert result.port == 27017
    assert result.bindip is None
    assert result.dbpath == '/var/lib/mongo'
    assert result.fork is True
    assert result.pidfilepath == '/var/run/mongodb/mongod.pid'
    assert result.syslog == 'file'
    assert result.logpath == '/var/log/mongodb/mongod.log'
    result = MongodbConf(context_wrap(NORMAL_CONF))
    assert result.is_yaml is False
    assert result.port is None
    assert result.bindip == '127.0.0.1'
    assert result.dbpath == '/var/lib/mongodb'
    assert result.fork == 'true'
    assert result.pidfilepath == '/var/run/mongodb/mongodb.pid'
    assert result.syslog is None
    assert result.logpath == '/var/log/mongodb/mongodb.log'
    assert result.get('abc') == ''
    assert result.get('def') is None
    result = MongodbConf(context_wrap(NORMAL_CONF_V1))
    assert result.is_yaml is False
    assert len(result.data) == 2
    assert result.get('logappend') == 'true'
    with pytest.raises(ParseException) as (e):
        MongodbConf(context_wrap(YAML_CONF_UNPARSABLE))
    assert 'mongod conf parse failed:' in str(e.value)
    with pytest.raises(ParseException) as (e):
        MongodbConf(context_wrap('#this is empty'))
    assert 'mongod.conf is empty or all lines are comments' in str(e.value)
    return