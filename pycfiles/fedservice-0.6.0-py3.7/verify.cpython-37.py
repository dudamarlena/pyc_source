# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/entity_statement/verify.py
# Compiled at: 2020-01-25 14:56:03
# Size of source mod 2**32: 3675 bytes
import logging
from cryptojwt import KeyBundle
from cryptojwt.jws.jws import factory
from fedservice.entity_statement.policy import apply_policy
from fedservice.entity_statement.policy import gather_policies
from fedservice.entity_statement.statement import Statement
logger = logging.getLogger(__name__)

def verify_trust_chain(es_list, key_jar):
    """

    :param es_list: List of entity statements. The entity's self-signed statement last.
    :param key_jar: A KeyJar instance
    :return: A sequence of verified entity statements
    """
    ves = []
    n = len(es_list) - 1
    for es in es_list:
        _jwt = factory(es)
        if _jwt:
            keys = key_jar.get_jwt_verify_keys(_jwt.jwt)
            res = _jwt.verify_compact(keys=keys)
            try:
                _jwks = res['jwks']
            except KeyError:
                if len(ves) != n:
                    raise ValueError('Missing signing JWKS')
            else:
                _kb = KeyBundle(keys=(_jwks['keys']))
                try:
                    old = key_jar.get_issuer_keys(res['sub'])
                except KeyError:
                    key_jar.add_kb(res['sub'], _kb)
                else:
                    new = [k for k in _kb if k not in old]
                    if new:
                        _kb.set(new)
                        key_jar.add_kb(res['sub'], _kb)
                ves.append(res)

    return ves


def trust_chain_expires_at(ves):
    exp = -1
    for v in ves:
        if exp >= 0:
            if v['exp'] < exp:
                exp = v['exp']
        else:
            exp = v['exp']

    return exp


def eval_policy_chain(chain, key_jar, entity_type):
    """

    :param chain: A trust chain
    :param key_jar: A key Jar
    :param entity_type:
    :return: tuple with federation ID, combined metadata policy and expiration time
    """
    ves = verify_trust_chain(chain, key_jar)
    tp_exp = trust_chain_expires_at(ves)
    return (
     ves[0]['iss'], gather_policies(ves[:-1], entity_type), tp_exp)


def eval_chain(chain, key_jar, entity_type, apply_policies=True):
    """

    :param chain: A chain of entity statements
    :param key_jar: A :py:class:`cryptojwt.key_jar.KeyJar` instance
    :param entity_type: Which type of metadata you want returned
    :param apply_policies: Apply policies to the metadata or not
    :returns: A Statement instances
    """
    ves = verify_trust_chain(chain, key_jar)
    tp_exp = trust_chain_expires_at(ves)
    statement = Statement(exp=tp_exp, verified_chain=ves)
    if apply_policies:
        if len(ves) > 1:
            combined_policy = gather_policies(ves[:-1], entity_type)
            try:
                metadata = ves[(-1)]['metadata'][entity_type]
            except KeyError:
                statement.metadata = None

            statement.metadata = apply_policy(metadata, combined_policy)
            statement.combined_policy = combined_policy
        else:
            statement.metadata = ves[0]['metadata'][entity_type]
            statement.combined_policy = {}
    else:
        statement.metadata = ves[(-1)]
    iss_path = [x['iss'] for x in ves]
    statement.fo = iss_path[0]
    iss_path.reverse()
    statement.iss_path = iss_path
    return statement