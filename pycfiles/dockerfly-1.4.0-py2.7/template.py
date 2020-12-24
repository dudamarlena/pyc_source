# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockerfly/runtime/template.py
# Compiled at: 2014-12-17 19:57:06
container = {'gateway': '192.168.159.1', 
   'eths': [
          [
           'testDockerflyv10',
           'eth0',
           '192.168.159.31/24']], 
   'image_name': '172.16.11.13:5000/brain/centos:centos6_sshd', 
   'container_name': 'dockerfly_1418176930_xxxx', 
   'run_cmd': '/usr/sbin/sshd -D', 
   'id': 3, 
   'status': 'running', 
   'last_modify_time': 1418176930.012}