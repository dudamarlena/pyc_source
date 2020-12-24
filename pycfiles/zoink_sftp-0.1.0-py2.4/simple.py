# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zoinksftp/example/simple.py
# Compiled at: 2009-02-04 09:36:01
"""
A very basic usage example. 

I'll expand this out a bit more and maybe add some command line handling. 
The power of this comes more from being able to programitically drive file
upload/downloading. If your on the command line I suggest using sftp 
instead ;)

Oisin Mulvihill
2009-02-04

"""
from zoinksftp import Connection

def main():
    """This is more for illustration purposes then anything else, as
    you'll need to change the details in order for it to work.
    """
    username = 'myuser'
    password = 'haveague33'
    myssh = Connection('example.com', username=username, password=password)
    myssh.put('ssh.py')
    myssh.get('mydata.db')
    myssh.getdir('/home/myuser/reports', '/tmp/reports')
    myssh.close()


if __name__ == '__main__':
    main()