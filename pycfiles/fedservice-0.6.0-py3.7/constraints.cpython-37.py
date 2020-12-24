# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/entity_statement/constraints.py
# Compiled at: 2019-11-11 05:19:22
# Size of source mod 2**32: 4868 bytes


def calculate_path_length(constraints, current_max_path_length, max_assigned):
    try:
        _max_len = constraints['max_path_length']
    except KeyError:
        if max_assigned:
            current_max_path_length -= 1
            return current_max_path_length
        return 0
    else:
        if max_assigned:
            new_current = current_max_path_length - 1
            if _max_len < new_current:
                return _max_len
            return new_current
        return _max_len


def remove_scheme(url):
    if url.startswith('https://'):
        return url[8:]
    if url.startswith('http://'):
        return url[7:]
    raise ValueError('Wrong scheme: %s', url)


def more_specific(a, b):
    a_part = remove_scheme(a).split('.')
    b_part = remove_scheme(b).split('.')
    if len(a_part) >= len(b_part):
        a_part.reverse()
        b_part.reverse()
        for _x, _y in zip(a_part, b_part):
            if _x != _y:
                if _y == '':
                    return True
                return False

        return True
    return False


def update_specs(new_constraints, old_constraints):
    _updated = []
    _replaced = False
    for _old in old_constraints:
        _replaced = False
        for _new in new_constraints:
            if more_specific(_new, _old):
                _updated.append(_new)
                _replaced = True

        if not _replaced:
            _updated.append(_old)

    return _updated


def add_constraints(new_constraints, naming_constraints):
    for key in ('permitted', 'excluded'):
        if not naming_constraints[key]:
            if key in new_constraints:
                if new_constraints[key]:
                    naming_constraints[key] = new_constraints[key][:]
                    continue
                else:
                    if not new_constraints[key]:
                        continue
            naming_constraints[key] = update_specs(new_constraints[key], naming_constraints[key])

    return naming_constraints


def update_naming_constraints(constraints, naming_constraints):
    try:
        new_constraints = constraints['naming_constraints']
    except KeyError:
        pass
    else:
        naming_constraints = add_constraints(new_constraints, naming_constraints)
    return naming_constraints


def excluded(subject_id, excluded_ids):
    for excl in excluded_ids:
        if more_specific(subject_id, excl):
            return True

    return False


def permitted(subject_id, permitted_id):
    for perm in permitted_id:
        if more_specific(subject_id, perm):
            return True

    return False


def meets_restrictions(trust_chain):
    """
    Verfies that the trust chain fulfills the constraints specified in it.

    :param trust_chain: A sequence of entity statements. The order is such that the leaf's is the
        last. The trust anchor's the first.
    :return: True is the constraints are fulfilled. False otherwise
    """
    current_max_path_length = 0
    max_assigned = False
    naming_constraints = {'permitted':None, 
     'excluded':None}
    for statement in trust_chain[:-1]:
        try:
            _constraints = statement['constraints']
        except KeyError:
            continue

        current_max_path_length = calculate_path_length(_constraints, current_max_path_length, max_assigned)
        if current_max_path_length < 0:
            return False
            naming_constraints = update_naming_constraints(_constraints, naming_constraints)
            if 'excluded' in naming_constraints:
                if naming_constraints['excluded']:
                    if excluded(statement['sub'], naming_constraints['excluded']):
                        return False
            if 'permitted' in naming_constraints and naming_constraints['permitted']:
                return permitted(statement['sub'], naming_constraints['permitted']) or False

    statement = trust_chain[(-1)]
    if 'excluded' in naming_constraints:
        if naming_constraints['excluded']:
            if excluded(statement['sub'], naming_constraints['excluded']):
                return False
    if 'permitted' in naming_constraints:
        if naming_constraints['permitted']:
            if not permitted(statement['sub'], naming_constraints['permitted']):
                return False
    return True