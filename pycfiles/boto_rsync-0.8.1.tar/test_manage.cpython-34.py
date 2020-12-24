# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/manage/test_manage.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 806 bytes
from boto.manage.server import Server
from boto.manage.volume import Volume
import time
print('--> Creating New Volume')
volume = Volume.create()
print(volume)
print('--> Creating New Server')
server_list = Server.create()
server = server_list[0]
print(server)
print('----> Waiting for Server to start up')
while server.status != 'running':
    print('*')
    time.sleep(10)

print('----> Server is running')
print('--> Run "df -k" on Server')
status = server.run('df -k')
print(status[1])
print('--> Now run volume.make_ready to make the volume ready to use on server')
volume.make_ready(server)
print('--> Run "df -k" on Server')
status = server.run('df -k')
print(status[1])
print('--> Do an "ls -al" on the new filesystem')
status = server.run('ls -al %s' % volume.mount_point)
print(status[1])