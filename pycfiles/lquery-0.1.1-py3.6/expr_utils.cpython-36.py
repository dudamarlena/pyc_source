# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lquery\expr_utils.py
# Compiled at: 2018-08-01 12:12:52
# Size of source mod 2**32: 1353 bytes
from .expr import IExpr, ParameterExpr, ConstExpr, AttrExpr, IndexExpr, BinaryExpr, CallExpr, LambdaExpr

def get_deep_indexes(index_expr: IndexExpr):
    """
    for example:

    `IndexExpr(x.a['size']['h'])` -> `['size', 'h'], AttrExpr(x.a)`.
    """
    fields = []
    cur_expr = index_expr
    while isinstance(cur_expr, IndexExpr):
        fields.append(cur_expr.name)
        cur_expr = cur_expr.expr

    fields.reverse()
    return (fields, cur_expr)


def require_argument(expr: IExpr) -> bool:
    """
    check is the `expr` reference or use argument to do some thing.
    """
    expr_type = type(expr)
    if expr_type is ParameterExpr:
        return True
    if expr_type is ConstExpr:
        return False
    if expr_type in (AttrExpr, IndexExpr):
        return require_argument(expr.expr)
    if expr_type is BinaryExpr:
        return require_argument(expr_type.left) or require_argument(expr_type.right)
    if expr_type is CallExpr:
        return any(require_argument(a) for a in list(expr.args) + list(expr.kwargs.values()))
    if expr_type is LambdaExpr:
        raise NotImplementedError
    raise NotImplementedError('any others ?')