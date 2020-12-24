# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ChernMachine/feeder.py
# Compiled at: 2018-05-11 11:13:11
# Size of source mod 2**32: 604 bytes
import uuid, os, tarfile
from Chern.utils import csys
from Chern.utils import metadata

def feed(impression, path):
    dst = os.path.join(os.environ['HOME'], '.ChernMachine/Storage', impression)
    print(dst)
    if not csys.exists(dst):
        print('Impression {} does not exists.'.format(impression))
        return
    uid = 'raw.' + uuid.uuid4().hex
    print(path, os.path.join(dst, uid, 'output'))
    csys.copy_tree(path, os.path.join(dst, uid, 'output'))
    config_file = metadata.ConfigFile(os.path.join(dst, uid, 'status.json'))
    config_file.write_variable('status', 'done')