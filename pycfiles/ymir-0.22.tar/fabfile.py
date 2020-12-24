# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/code/ymir/ymir/skeleton/fabfile.py
# Compiled at: 2016-07-13 22:08:18
"""
\x1b[31mYmir Automation:\x1b[0m
  This is the \x1b[35mDemo\x1b[0m Service
"""
from fabric import api
from ymir import load_service_from_json, guess_service_json_file
YMIR_SERVICE_JSON = guess_service_json_file(default='service.json')
service = load_service_from_json(YMIR_SERVICE_JSON)
service.fabric_install()

@api.task
def deploy(branch='master'):
    """ example usage: "fab deploy:branch=master" """
    service.report(('deploy for branch {0} -> {1} is not defined yet').format(branch, service))


@api.task
def tail_syslog():
    """ example: tail syslog on remote server """
    with service.ssh_ctx():
        api.sudo('tail /var/log/syslog')