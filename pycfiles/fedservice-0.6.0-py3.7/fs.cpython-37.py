# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/metadata_api/fs.py
# Compiled at: 2019-08-29 03:47:22
# Size of source mod 2**32: 1991 bytes
import json, logging, os
from urllib.parse import urlparse
from cryptojwt.key_jar import KeyJar
from fedservice.entity_statement.create import create_entity_statement
logger = logging.getLogger(__name__)

def mk_path(*args):
    _part = []
    for arg in args:
        if arg.startswith('https://') or arg.startswith('http://'):
            _ip = urlparse(arg)
            _part.append(format('_'.join(_ip.path[1:].split('/'))))
        else:
            _part.append(arg)

    _dir = '/'.join(_part)
    if not os.path.isdir(_dir):
        return
    return _dir


def read_info(dir, sub, typ='metadata'):
    file_name = os.path.join(dir, '{}.{}.json'.format(sub, typ))
    if os.path.isfile(file_name):
        return json.loads(open(file_name).read())
    return


def get_authority_hints(iss, sub, root_dir):
    _auth = read_info(os.path.join(root_dir, iss), sub, 'authority')
    if _auth:
        return _auth
    return {}


def make_entity_statement(iss, root_dir='.', sub=''):
    kj = KeyJar()
    if iss.startswith('https://'):
        iss_id = iss
        iss = iss[len('https://'):]
    else:
        iss_id = 'https://{}'.format(iss)
    _jwks = read_info(os.path.join(root_dir, iss), iss, 'jwks')
    kj.import_jwks(_jwks, iss_id)
    if not sub:
        sub = iss
    else:
        if sub.startswith('https://'):
            sub_id = sub
            sub = sub[len('https://'):]
        else:
            sub_id = 'https://{}'.format(sub)
        _jwks = read_info(os.path.join(root_dir, iss), sub, 'jwks')
        kj.import_jwks(_jwks, sub_id)
        metadata = read_info(os.path.join(root_dir, iss), sub, 'metadata')
        policy = read_info(os.path.join(root_dir, iss), sub, 'policy')
        _auth = get_authority_hints(iss, sub, root_dir)
        if _auth:
            _jwt = create_entity_statement(iss_id, sub_id, kj, metadata, policy, _auth)
        else:
            _jwt = create_entity_statement(iss_id, sub_id, kj, metadata, policy)
    return _jwt