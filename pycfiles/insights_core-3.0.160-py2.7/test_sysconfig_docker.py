# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_docker.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import DockerSysconfig
from insights.tests import context_wrap
DOCKER_SYSCONFIG_STD = "\n# /etc/sysconfig/docker\n\n# Modify these options if you want to change the way the docker daemon runs\nOPTIONS='--selinux-enabled'\n\nDOCKER_CERT_PATH=/etc/docker\n\n# If you want to add your own registry to be used for docker search and docker\n# pull use the ADD_REGISTRY option to list a set of registries, each prepended\n# with --add-registry flag. The first registry added will be the first registry\n# searched.\nADD_REGISTRY='--add-registry registry.access.redhat.com'\n\n# If you want to block registries from being used, uncomment the BLOCK_REGISTRY\n# option and give it a set of registries, each prepended with --block-registry\n# flag. For example adding docker.io will stop users from downloading images\n# from docker.io\n# BLOCK_REGISTRY='--block-registry'\n\n# If you have a registry secured with https but do not have proper certs\n# distributed, you can tell docker to not look for full authorization by\n# adding the registry to the INSECURE_REGISTRY line and uncommenting it.\n# INSECURE_REGISTRY='--insecure-registry'\n\n# On an SELinux system, if you remove the --selinux-enabled option, you\n# also need to turn on the docker_transition_unconfined boolean.\n# setsebool -P docker_transition_unconfined 1\n\n# Location used for temporary files, such as those created by\n# docker load and build operations. Default is /var/lib/docker/tmp\n# Can be overriden by setting the following environment variable.\n# DOCKER_TMPDIR=/var/tmp\n\n# Controls the /etc/cron.daily/docker-logrotate cron job status.\n# To disable, uncomment the line below.\n# LOGROTATE=false\n"

def test_standard_content():
    context = context_wrap(DOCKER_SYSCONFIG_STD, 'etc/sysconfig/docker')
    sysconf = DockerSysconfig(context)
    assert sorted(sysconf.keys()) == sorted(['OPTIONS', 'DOCKER_CERT_PATH', 'ADD_REGISTRY'])
    assert 'OPTIONS' in sysconf
    assert sysconf['OPTIONS'] == '--selinux-enabled'
    assert sysconf.options == '--selinux-enabled'
    assert 'DOCKER_CERT_PATH' in sysconf
    assert sysconf['DOCKER_CERT_PATH'] == '/etc/docker'
    assert 'ADD_REGISTRY' in sysconf
    assert sysconf['ADD_REGISTRY'] == '--add-registry registry.access.redhat.com'
    assert sysconf.unparsed_lines == []