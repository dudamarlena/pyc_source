# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/entity_statement/policy.py
# Compiled at: 2019-12-08 20:00:35
# Size of source mod 2**32: 10122 bytes
import logging
logger = logging.getLogger(__name__)

class PolicyError(Exception):
    pass


def combine_subset_of(s1, s2):
    return list(set(s1).intersection(set(s2)))


def combine_superset_of(s1, s2):
    return list(set(s1).intersection(set(s2)))


def combine_one_of(s1, s2):
    return list(set(s1).intersection(set(s2)))


def combine_add(s1, s2):
    if isinstance(s1, list):
        set1 = set(s1)
    else:
        set1 = {
         s1}
    if isinstance(s2, list):
        set2 = set(s2)
    else:
        set2 = {
         s2}
    return list(set1.union(set2))


POLICY_FUNCTIONS = {
 'subset_of', 'superset_of', 'one_of', 'add', 'value', 'default', 'essential'}
OP2FUNC = {'subset_of':combine_subset_of, 
 'superset_of':combine_superset_of, 
 'one_of':combine_one_of, 
 'add':combine_add}
ALLOWED_COMBINATIONS = [
 {
  'superset_of', 'subset_of'},
 {
  'default', 'one_of'},
 {
  'default', 'subset_of'},
 {
  'essential', 'subset_of'},
 {
  'default', 'superset_of'},
 {
  'essential', 'superset_of'},
 {
  'essential', 'one_of'},
 {
  'essential', 'add'},
 {
  'essential', 'value'},
 {
  'essential', 'default'},
 {
  'default', 'subset_of', 'superset_of'},
 {
  'essential', 'subset_of', 'superset_of'}]

def weed(policy):
    """
    Remove policy functions that are not part of the standard

    :param policy: Policy definition
    :return: Policy definition with all non-standard keys weeded out
    """
    return set(policy.keys()).difference(POLICY_FUNCTIONS)


def do_sub_one_super_add(superior, child, policy):
    if policy in superior and policy in child:
        comb = OP2FUNC[policy](superior[policy], child[policy])
        if comb:
            return comb
        raise PolicyError("Value sets doesn't overlap")
    else:
        if policy in superior:
            return superior[policy]
        if policy in child:
            return child[policy]


def do_value(superior, child, policy):
    if policy in superior and policy in child:
        if superior[policy] == child[policy]:
            return superior[policy]
        raise PolicyError('Not allowed to combine values')
    else:
        if policy in superior:
            return superior[policy]
        if policy in child:
            return child[policy]


def do_default(superior, child, policy):
    if policy in superior and policy in child:
        if superior['default'] == child['default']:
            return superior['default']
        raise PolicyError('Not allowed to change default')
    else:
        if policy in superior:
            return superior[policy]
        if policy in child:
            return child[policy]


def do_essential(superior, child, policy):
    if policy in superior and policy in child:
        if not superior[policy]:
            if child['essential']:
                return True
        return superior[policy]
    else:
        if policy in superior:
            return superior[policy]
        if policy in child:
            return True


DO_POLICY = {'superset_of':do_sub_one_super_add, 
 'subset_of':do_sub_one_super_add, 
 'one_of':do_sub_one_super_add, 
 'add':do_sub_one_super_add, 
 'value':do_value, 
 'default':do_default, 
 'essential':do_essential}

def combine_claim_policy(superior, child):
    """
    Combine policy rules

    :param superior: Superior policy
    :param child: Intermediates policy
    """
    comb_policy = set(superior.keys()).union(set(child.keys()))
    comb_policy = comb_policy.intersection(POLICY_FUNCTIONS)
    if len(comb_policy) > 3:
        raise PolicyError('Not allowed combination of policies')
    else:
        if len(comb_policy) in (2, 3):
            if comb_policy not in ALLOWED_COMBINATIONS:
                raise PolicyError('Not allowed combination of policies')
    rule = {}
    for policy in comb_policy:
        rule[policy] = DO_POLICY[policy](superior, child, policy)

    if comb_policy == {'superset_of', 'subset_of'}:
        if set(rule['superset_of']).difference(set(rule['subset_of'])):
            raise PolicyError('superset_of not a super set of subset_of')
    else:
        if comb_policy == {'superset_of', 'subset_of', 'default'}:
            if set(rule['superset_of']).difference(set(rule['subset_of'])):
                raise PolicyError('superset_of not a super set of subset_of')
            if set(rule['default']).difference(set(rule['subset_of'])):
                raise PolicyError('default not a sub set of subset_of')
            if set(rule['superset_of']).difference(set(rule['default'])):
                raise PolicyError('default not a super set of subset_of')
        elif comb_policy == {'subset_of', 'default'}:
            if set(rule['default']).difference(set(rule['subset_of'])):
                raise PolicyError('default not a sub set of subset_of')
        elif comb_policy == {'superset_of', 'default'}:
            if set(rule['superset_of']).difference(set(rule['default'])):
                raise PolicyError('default not a super set of subset_of')
        elif comb_policy == {'one_of', 'default'}:
            if isinstance(rule['default'], list):
                if set(rule['default']).difference(set(rule['one_of'])):
                    raise PolicyError('default not a super set of one_of')
            elif {
             rule['default']}.difference(set(rule['one_of'])):
                raise PolicyError('default not a super set of one_of')
        return rule


def combine_policy(superior, child):
    res = {}
    sup_set = set(superior.keys())
    chi_set = set(child.keys())
    for claim in set(sup_set).intersection(chi_set):
        res[claim] = combine_claim_policy(superior[claim], child[claim])

    for claim in sup_set.difference(chi_set):
        res[claim] = superior[claim]

    for claim in chi_set.difference(sup_set):
        res[claim] = child[claim]

    return res


def gather_policies(chain, entity_type):
    """
    Gather and combine all the metadata policies that are defined in the trust chain
    :param chain: A list of Entity Statements
    :return: The combined metadata policy
    """
    try:
        combined_policy = chain[0]['metadata_policy'][entity_type]
    except KeyError:
        combined_policy = {}

    for es in chain[1:]:
        try:
            child = es['metadata_policy'][entity_type]
        except KeyError:
            pass
        else:
            combined_policy = combine_policy(combined_policy, child)

    return combined_policy


def union(val1, val2):
    if isinstance(val1, list):
        base = set(val1)
    else:
        base = {
         val1}
    if isinstance(val2, list):
        ext = set(val2)
    else:
        ext = {
         val2}
    return base.union(ext)


def apply_policy(metadata, policy):
    """
    Apply a metadata policy to a metadata statement

    :param metadata: A metadata statement
    :param policy: A metadata policy
    :return: A metadata statement that adheres to a metadata policy
    """
    metadata_set = set(metadata.keys())
    policy_set = set(policy.keys())
    for claim in metadata_set.intersection(policy_set):
        if 'subset_of' in policy[claim]:
            _val = set(policy[claim]['subset_of']).intersection(set(metadata[claim]))
            if _val:
                metadata[claim] = list(_val)
            else:
                raise PolicyError('{} not subset of {}'.format(metadata[claim], policy[claim]['subset_of']))
        else:
            if 'superset_of' in policy[claim]:
                if set(policy[claim]['superset_of']).difference(set(metadata[claim])):
                    raise PolicyError('{} not superset of {}'.format(metadata[claim], policy[claim]['superset_of']))
                else:
                    continue
            else:
                if 'one_of' in policy[claim]:
                    if isinstance(metadata[claim], list):
                        _claim = None
                        for c in metadata[claim]:
                            if c in policy[claim]['one_of']:
                                _claim = c
                                break

                        if _claim:
                            metadata[claim] = _claim
                        else:
                            raise PolicyError('None of {} among {}'.format(metadata[claim], policy[claim]['one_of']))
                    elif metadata[claim] in policy[claim]['one_of']:
                        pass
                    else:
                        raise PolicyError('{} not among {}'.format(metadata[claim], policy[claim]['one_of']))
            if 'add' in policy[claim]:
                metadata[claim] = list(union(metadata[claim], policy[claim]['add']))

    for claim in policy_set.difference(metadata_set):
        if 'default' in policy[claim]:
            metadata[claim] = policy[claim]['default']
        if 'essential' in policy[claim]:
            if policy[claim]['essential']:
                raise PolicyError("Essential claim '{}' missing".format(claim))
            if 'add' in policy[claim]:
                metadata[claim] = policy[claim]['add']
            if 'value' in policy[claim]:
                metadata[claim] = policy[claim]['value']

    return metadata


def diff2policy(new, old):
    res = {}
    for claim in set(new).intersection(set(old)):
        if new[claim] == old[claim]:
            continue
        else:
            res[claim] = {'value': new[claim]}

    for claim in set(new).difference(set(old)):
        if claim in ('contacts', ):
            res[claim] = {'add': new[claim]}
        else:
            res[claim] = {'value': new[claim]}

    return res