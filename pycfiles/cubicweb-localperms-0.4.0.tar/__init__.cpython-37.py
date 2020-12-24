# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dlaxalde/src/cw/cubes/localperms/cubicweb_localperms/__init__.py
# Compiled at: 2019-03-13 06:52:19
# Size of source mod 2**32: 3135 bytes
"""cubicweb-localperms application package

allow definition of local permissions
"""
from rql.utils import quote
from logilab.common.deprecation import deprecated
from cubicweb.schema import ERQLExpression, RRQLExpression

def _perm(names):
    if isinstance(names, (list, tuple)):
        if len(names) == 1:
            names = quote(names[0])
        else:
            names = 'IN (%s)' % ','.join((quote(name) for name in names))
    else:
        names = quote(names)
    return ' require_permission P, P name %s, U has_group_permission P' % names


def xperm(*names):
    return 'X' + _perm(names)


def xexpr(*names):
    return ERQLExpression(xperm(*names))


_XREXPR_OPTIONS = frozenset(('role', 'etype'))

def xrexpr(relation, *names, **options):
    """return an :class:`ERQLExpression` where X is related to an Y variable
    through `relation`, by default as subject, but you can specify 'object using
    the `role` keyword argument. The Y variable is itself linked to a
    :class:`CWPermission` entity which should have one of the given `names`.

    You can also specify the entity type for X using the `etype` keyword
    argument.

    Examples:

    >>> xrexpr('a_relation', 'read', 'write').expression
    u'X a_relation Y, Y require_permission P, P name IN ("read", "write"),     U has_group_permission P'
    >>> xrexpr('a_relation', 'read', role='object').expression
    u'Y a_relation X, Y require_permission P, P name "read",     U has_group_permission P'
    >>> xrexpr('a_relation', 'read', etype='MyEType').expression
    u'X a_relation Y, X is MyEType, Y require_permission P, P name "read",     U has_group_permission P'
    """
    if set(options) - _XREXPR_OPTIONS:
        raise AssertionError('unknown option specified: %s' % (set(options) - _XREXPR_OPTIONS))
    else:
        role = options.get('role', 'subject')
        assert role in ('subject', 'object'), 'bad role %s' % role
        if role == 'subject':
            rql = 'X %s Y' % relation
        else:
            rql = 'Y %s X' % relation
    if options.get('etype'):
        rql += ', X is %s' % options.get('etype')
    return ERQLExpression('%s, Y %s' % (rql, _perm(names)))


def sexpr(*names):
    return RRQLExpression('S' + _perm(names), 'S')


def restricted_sexpr(restriction, *names):
    rql = '%s, %s' % (restriction, 'S' + _perm(names))
    return RRQLExpression(rql, 'S')


def restricted_oexpr(restriction, *names):
    rql = '%s, %s' % (restriction, 'O' + _perm(names))
    return RRQLExpression(rql, 'O')


def oexpr(*names):
    return RRQLExpression('O' + _perm(names), 'O')


def relxperm(rel, role, *names):
    if not role in ('subject', 'object'):
        raise AssertionError
    elif role == 'subject':
        zxrel = ', X %s Z' % rel
    else:
        zxrel = ', Z %s X' % rel
    return 'Z' + _perm(names) + zxrel


def relxexpr(rel, role, *names):
    return ERQLExpression(relxperm(rel, role, *names))


@deprecated('use xrexpr(..., role="object") instead')
def xorexpr(relation, etype, *names):
    return ERQLExpression('Y %s X, X is %s, Y %s' % (relation, etype, _perm(names)))