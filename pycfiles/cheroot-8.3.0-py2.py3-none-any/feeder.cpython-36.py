# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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