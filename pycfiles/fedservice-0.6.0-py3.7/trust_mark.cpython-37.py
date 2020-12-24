# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/entity_statement/trust_mark.py
# Compiled at: 2020-01-25 14:57:32
# Size of source mod 2**32: 2470 bytes
from cryptojwt import JWT
from fedservice import branch2lists
from fedservice import eval_chain
from fedservice.entity_statement.collect import verify_self_signed_signature
from fedservice.exception import ConstraintError
from fedservice.message import TrustMark

def create_trust_mark(entity_id, key_jar, trust_mark_id, subject='', lifetime=0, trust_mark='', reference=''):
    """
    Create Trust Mark.

    :param entity_id: The issuers entity_id
    :param key_jar: A KeyJar that contains useful keys
    :param trust_mark_id: The Trust Mark identifier
    :param subject: The subject's id
    :param lifetime: For how long the trust mark should be valid (0=for ever)
    :param trust_mark: A URL pointing to a graphic trust mark
    :param reference: A URL pointing to reference material for this trust mark
    :return: A signed JWT containing the provided information
    """
    _tm = TrustMark(id=trust_mark_id)
    if trust_mark:
        _tm['mark'] = trust_mark
    else:
        if reference:
            _tm['ref'] = reference
        if subject:
            _tm['sub'] = subject
        else:
            _tm['sub'] = entity_id
    _jwt = JWT(key_jar=key_jar, iss=entity_id, lifetime=lifetime)
    return _jwt.pack(_tm)


def unpack_trust_mark(token, keyjar, entity_id):
    _jwt = JWT(key_jar=keyjar, msg_cls=TrustMark, allowed_sign_algs=['RS256'])
    _tm = _jwt.unpack(token)
    _tm.verify(entity_id=entity_id)
    return _tm


def get_trust_mark(federation_entity, token, entity_id, trust_anchor_id):
    _tm = unpack_trust_mark(token, federation_entity.key_jar, entity_id)
    entity_config = federation_entity.get_configuration_information(_tm['iss'])
    statements = federation_entity.collect_metadata_statements(entity_config, 'federation_entity')
    statement = None
    for s in statements:
        if s.iss_path[(-1)] == trust_anchor_id:
            statement = s
            break

    if _tm['sub'] != _tm['iss']:
        if len(statement.iss_path) > 2:
            raise ConstraintError('Trust chain too long')
    return _tm