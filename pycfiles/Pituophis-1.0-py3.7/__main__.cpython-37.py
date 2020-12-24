# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pituophis/__main__.py
# Compiled at: 2019-05-24 19:14:13
# Size of source mod 2**32: 2037 bytes
import pituophis, os, sys
if len(sys.argv) < 2:
    print('Subcommands:')
    print('  dev_server: run a simple server using the current working directory as a publish directory.')
    print('  new_server: create a server script.')
else:
    if sys.argv[1] == 'dev_server':
        cfg = {'host':'127.0.0.1', 
         'port':7075,  'pub_dir':'./',  'tls':False}
        print('Publish directory: ' + os.path.abspath(cfg['pub_dir']))
        pituophis.serve((cfg['host']), (cfg['port']), pub_dir=(cfg['pub_dir']), tls=(cfg['tls']))